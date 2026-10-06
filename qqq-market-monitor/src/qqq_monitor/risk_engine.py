from qqq_monitor.models import Indicators, RiskAssessment


def assess_risk(price: float, indicators: Indicators) -> RiskAssessment:
    """Produce an explainable monitoring status, not an investment recommendation."""
    score = 0
    signals: list[str] = []

    rsi = indicators.rsi_14
    if rsi is not None and rsi >= 70:
        score += 2
        signals.append(f"RSI {rsi:.2f}，处于相对高位区间")
    elif rsi is not None and rsi <= 30:
        score += 2
        signals.append(f"RSI {rsi:.2f}，处于相对低位区间")
    elif rsi is not None and (rsi >= 60 or rsi <= 40):
        score += 1
        signals.append(f"RSI {rsi:.2f}，市场动量偏强或偏弱")

    if indicators.sma_200 is not None and price < indicators.sma_200:
        score += 1
        signals.append("价格低于 200 日均线，长期趋势需关注")

    if indicators.annualized_volatility is not None and indicators.annualized_volatility >= 0.30:
        score += 1
        signals.append(
            f"年化波动率约 {indicators.annualized_volatility:.1%}，近期波动偏高"
        )

    if indicators.max_drawdown is not None and indicators.max_drawdown <= -0.20:
        score += 1
        signals.append(f"观察期最大回撤约 {indicators.max_drawdown:.1%}")

    if score >= 4:
        level = "HIGH"
        summary = "多个风险信号同时出现，建议重点关注波动和回撤。"
    elif score >= 2:
        level = "MEDIUM"
        summary = "存在需要关注的市场信号，建议结合更多信息判断。"
    else:
        level = "LOW"
        summary = "当前规则未识别出明显的高风险信号。"

    if not signals:
        signals.append("当前规则未触发额外风险信号")

    return RiskAssessment(level=level, score=score, signals=signals, summary=summary)
