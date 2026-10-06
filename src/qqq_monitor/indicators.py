from __future__ import annotations

import math
from statistics import stdev
from typing import Iterable, Optional

from qqq_monitor.models import Indicators


def _values(values: Iterable[float]) -> list[float]:
    result = [float(value) for value in values]
    if any(not math.isfinite(value) for value in result):
        raise ValueError("Price series contains a non-finite value")
    return result


def moving_average(closes: Iterable[float], period: int) -> Optional[float]:
    values = _values(closes)
    if period <= 0:
        raise ValueError("period must be positive")
    if len(values) < period:
        return None
    return sum(values[-period:]) / period


def rsi_wilder(closes: Iterable[float], period: int = 14) -> Optional[float]:
    """Calculate RSI using Wilder's smoothing method."""
    values = _values(closes)
    if period <= 0:
        raise ValueError("period must be positive")
    if len(values) < period + 1:
        return None

    deltas = [current - previous for previous, current in zip(values, values[1:])]
    gains = [max(delta, 0.0) for delta in deltas]
    losses = [max(-delta, 0.0) for delta in deltas]
    average_gain = sum(gains[:period]) / period
    average_loss = sum(losses[:period]) / period

    for gain, loss in zip(gains[period:], losses[period:]):
        average_gain = ((average_gain * (period - 1)) + gain) / period
        average_loss = ((average_loss * (period - 1)) + loss) / period

    if average_loss == 0:
        return 100.0 if average_gain > 0 else 50.0
    relative_strength = average_gain / average_loss
    return round(100 - (100 / (1 + relative_strength)), 2)


def annualized_volatility(closes: Iterable[float], trading_days: int = 252) -> Optional[float]:
    values = _values(closes)
    returns = [current / previous - 1 for previous, current in zip(values, values[1:]) if previous]
    if len(returns) < 2:
        return None
    return stdev(returns) * math.sqrt(trading_days)


def max_drawdown(closes: Iterable[float]) -> Optional[float]:
    values = _values(closes)
    if not values:
        return None
    peak = values[0]
    worst = 0.0
    for value in values:
        peak = max(peak, value)
        worst = min(worst, value / peak - 1)
    return worst


def calculate_indicators(closes: Iterable[float]) -> Indicators:
    values = _values(closes)
    return Indicators(
        rsi_14=rsi_wilder(values, 14),
        sma_20=moving_average(values, 20),
        sma_50=moving_average(values, 50),
        sma_200=moving_average(values, 200),
        annualized_volatility=annualized_volatility(values),
        max_drawdown=max_drawdown(values),
    )
