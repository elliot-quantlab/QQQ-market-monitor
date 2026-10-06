from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class MarketData:
    symbol: str
    price: float
    previous_close: float
    change_pct: float
    closes: list[float]
    market_date: datetime
    trailing_pe: Optional[float]


@dataclass(frozen=True)
class Indicators:
    rsi_14: Optional[float]
    sma_20: Optional[float]
    sma_50: Optional[float]
    sma_200: Optional[float]
    annualized_volatility: Optional[float]
    max_drawdown: Optional[float]


@dataclass(frozen=True)
class RiskAssessment:
    level: str
    score: int
    signals: list[str]
    summary: str
