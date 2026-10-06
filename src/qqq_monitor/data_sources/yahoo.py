from __future__ import annotations

import logging
from typing import Any, Optional

import yfinance as yf

from qqq_monitor.models import MarketData

logger = logging.getLogger(__name__)


class MarketDataError(RuntimeError):
    """Raised when market data cannot be retrieved or validated."""


def _to_float(value: Any) -> Optional[float]:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if number == number else None


def fetch_market_data(symbol: str) -> MarketData:
    """Fetch one year of daily closes and the latest available valuation.

    Yahoo Finance is used through yfinance rather than scraping HTML. Valuation
    data is optional because ETF metadata is not guaranteed to be available.
    """
    ticker = yf.Ticker(symbol)
    try:
        history = ticker.history(period="1y", interval="1d", auto_adjust=False)
    except Exception as exc:
        raise MarketDataError(f"Unable to fetch price history for {symbol}: {exc}") from exc

    if history.empty or "Close" not in history:
        raise MarketDataError(f"No usable price history returned for {symbol}")

    closes = [float(value) for value in history["Close"].dropna().tolist()]
    if len(closes) < 2:
        raise MarketDataError(f"At least two closing prices are required for {symbol}")

    price = closes[-1]
    previous_close = closes[-2]
    if previous_close == 0:
        raise MarketDataError("Previous close is zero; change percentage is undefined")

    market_date = history.dropna(subset=["Close"]).index[-1].to_pydatetime()
    trailing_pe: Optional[float] = None
    try:
        info = ticker.info
        trailing_pe = _to_float(info.get("trailingPE"))
    except Exception as exc:
        logger.warning("Valuation metadata unavailable for %s: %s", symbol, exc)

    return MarketData(
        symbol=symbol,
        price=price,
        previous_close=previous_close,
        change_pct=(price / previous_close - 1) * 100,
        closes=closes,
        market_date=market_date,
        trailing_pe=trailing_pe,
    )
