import unittest

from qqq_monitor.indicators import (
    annualized_volatility,
    max_drawdown,
    moving_average,
    rsi_wilder,
)


class IndicatorTests(unittest.TestCase):
    def test_moving_average(self):
        self.assertEqual(moving_average([1, 2, 3, 4, 5], 3), 4.0)
        self.assertIsNone(moving_average([1, 2], 3))

    def test_rsi_rising_series_is_high(self):
        values = list(range(1, 20))
        self.assertEqual(rsi_wilder(values, 14), 100.0)

    def test_max_drawdown(self):
        self.assertAlmostEqual(max_drawdown([100, 120, 90, 110]), -0.25)

    def test_volatility_requires_two_returns(self):
        self.assertIsNone(annualized_volatility([100, 101]))


if __name__ == "__main__":
    unittest.main()
