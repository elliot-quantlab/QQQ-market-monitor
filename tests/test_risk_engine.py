import unittest

from qqq_monitor.models import Indicators
from qqq_monitor.risk_engine import assess_risk


class RiskEngineTests(unittest.TestCase):
    def test_high_risk_has_explainable_signals(self):
        indicators = Indicators(
            rsi_14=75,
            sma_20=110,
            sma_50=120,
            sma_200=130,
            annualized_volatility=0.35,
            max_drawdown=-0.25,
        )
        result = assess_risk(100, indicators)
        self.assertEqual(result.level, "HIGH")
        self.assertGreaterEqual(len(result.signals), 3)

    def test_low_risk_when_no_rule_is_triggered(self):
        indicators = Indicators(50, 99, 98, 95, 0.10, -0.05)
        result = assess_risk(100, indicators)
        self.assertEqual(result.level, "LOW")


if __name__ == "__main__":
    unittest.main()
