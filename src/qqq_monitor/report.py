from __future__ import annotations

from datetime import datetime
from html import escape

from qqq_monitor.models import Indicators, MarketData, RiskAssessment


def _number(value: float | None, suffix: str = "", digits: int = 2) -> str:
    return "N/A" if value is None else f"{value:.{digits}f}{suffix}"


def render_html(
    market: MarketData,
    indicators: Indicators,
    risk: RiskAssessment,
    generated_at: datetime,
) -> str:
    change_color = "#16803c" if market.change_pct >= 0 else "#c62828"
    change_symbol = "▲" if market.change_pct >= 0 else "▼"
    risk_color = {"LOW": "#16803c", "MEDIUM": "#b26a00", "HIGH": "#c62828"}[risk.level]
    signal_html = "".join(f"<li>{escape(signal)}</li>" for signal in risk.signals)

    volatility = _number(indicators.annualized_volatility, "%", 1)
    drawdown = _number(indicators.max_drawdown, "%", 1)
    return f"""<!doctype html>
<html lang="zh-CN">
<head><meta charset="utf-8"><title>{escape(market.symbol)} Daily Market Briefing</title></head>
<body style="margin:0;background:#f3f5f7;font-family:Arial,'Microsoft YaHei',sans-serif;color:#1f2937;">
<main style="max-width:680px;margin:24px auto;padding:24px;background:#fff;border-radius:12px;">
  <h1 style="margin-top:0;">{escape(market.symbol)} 每日市场简报</h1>
  <p style="color:#6b7280;">行情日期：{market.market_date:%Y-%m-%d}　生成时间：{generated_at:%Y-%m-%d %H:%M:%S %Z}</p>
  <table style="width:100%;border-collapse:collapse;">
    <tr><td style="padding:10px 0;">最新收盘价</td><td style="text-align:right;font-weight:bold;">{market.price:.2f}</td></tr>
    <tr><td style="padding:10px 0;">日涨跌幅</td><td style="text-align:right;color:{change_color};font-weight:bold;">{change_symbol} {market.change_pct:.2f}%</td></tr>
    <tr><td style="padding:10px 0;">Trailing PE</td><td style="text-align:right;">{_number(market.trailing_pe)}</td></tr>
    <tr><td style="padding:10px 0;">RSI (14)</td><td style="text-align:right;">{_number(indicators.rsi_14)}</td></tr>
    <tr><td style="padding:10px 0;">20 / 50 / 200 日均线</td><td style="text-align:right;">{_number(indicators.sma_20)} / {_number(indicators.sma_50)} / {_number(indicators.sma_200)}</td></tr>
    <tr><td style="padding:10px 0;">年化波动率</td><td style="text-align:right;">{volatility}</td></tr>
    <tr><td style="padding:10px 0;">观察期最大回撤</td><td style="text-align:right;">{drawdown}</td></tr>
  </table>
  <section style="margin-top:20px;padding:16px;border-left:5px solid {risk_color};background:#fafafa;">
    <h2 style="margin:0 0 8px;color:{risk_color};">风险状态：{risk.level}</h2>
    <p>{escape(risk.summary)}</p>
    <ul>{signal_html}</ul>
  </section>
  <p style="margin-bottom:0;color:#6b7280;font-size:12px;">本报告仅用于信息整理和研究，不构成投资建议。数据来自 Yahoo Finance，估值字段可能因数据源限制缺失。</p>
</main>
</body></html>"""


def render_plain_text(market: MarketData, indicators: Indicators, risk: RiskAssessment) -> str:
    signals = "\n".join(f"- {signal}" for signal in risk.signals)
    return (
        f"{market.symbol} 每日市场简报\n"
        f"行情日期：{market.market_date:%Y-%m-%d}\n"
        f"最新收盘价：{market.price:.2f}\n"
        f"日涨跌幅：{market.change_pct:.2f}%\n"
        f"Trailing PE：{_number(market.trailing_pe)}\n"
        f"RSI(14)：{_number(indicators.rsi_14)}\n"
        f"风险状态：{risk.level}\n{risk.summary}\n{signals}\n\n"
        "本报告仅用于信息整理和研究，不构成投资建议。"
    )
