import unittest

from shop.events import balance_change


class BalanceChangeTest(unittest.TestCase):
    def test_refund_credits(self):
        self.assertEqual(balance_change({"type": "ref", "amount_cents": 500}), 500)

    def test_sale_charges(self):
        self.assertEqual(balance_change({"type": "sale", "amount_cents": 500}), -500)


if __name__ == "__main__":
    unittest.main()
