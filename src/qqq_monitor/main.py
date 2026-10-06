from __future__ import annotations

import logging
from datetime import datetime

from qqq_monitor.config import ConfigurationError, Settings
from qqq_monitor.data_sources.yahoo import fetch_market_data
from qqq_monitor.indicators import calculate_indicators
from qqq_monitor.notifier import send_email
from qqq_monitor.report import render_html, render_plain_text
from qqq_monitor.risk_engine import assess_risk

logger = logging.getLogger(__name__)


def main() -> int:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s - %(message)s",
    )

    try:
        settings = Settings.from_env()
        settings.output_dir.mkdir(parents=True, exist_ok=True)

        market = fetch_market_data(settings.symbol)
        indicators = calculate_indicators(market.closes)
        risk = assess_risk(market.price, indicators)
        generated_at = datetime.now(settings.timezone)
        html = render_html(market, indicators, risk, generated_at)
        plain_text = render_plain_text(market, indicators, risk)

        report_path = settings.output_dir / f"{settings.symbol.lower()}_{generated_at:%Y%m%d_%H%M%S}.html"
        report_path.write_text(html, encoding="utf-8")
        logger.info("HTML report saved to %s", report_path)

        subject = f"{market.symbol} Daily Market Briefing - {market.market_date:%Y-%m-%d}"
        send_email(settings, subject, plain_text, html)
        logger.info("Completed successfully; risk level=%s", risk.level)
        return 0
    except ConfigurationError:
        logger.exception("Invalid configuration")
        return 1
    except Exception:
        logger.exception("Report generation failed")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
