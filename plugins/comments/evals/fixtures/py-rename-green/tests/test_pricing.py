import unittest

from shop.pricing import with_tax


class WithTaxTest(unittest.TestCase):
    def test_adds_tax(self):
        self.assertEqual(with_tax(1000, 25), 1250)

    def test_rounds_to_whole_cents(self):
        self.assertEqual(with_tax(999, 15), 1149)


if __name__ == "__main__":
    unittest.main()
