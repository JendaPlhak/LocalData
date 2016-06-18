import unittest

from parser import HOUSE_NUM_PATTERN, PARCEL_NUM_PATTERN, PRICE_PATTERN


class TestRegexes(unittest.TestCase):

    def test_house_num(self):
        cases = {
            "č. p. 13": "13",
            "č.p. 15": "15",
            "čp. 17": "17",
        }

        for c, r in cases.items():
            self.assertIsNotNone(HOUSE_NUM_PATTERN.search(c), c)
            self.assertEqual(HOUSE_NUM_PATTERN.search(c).group("num"), r)

    def test_parcel_num(self):
        cases = {
            "text parc. č. 13 text": "13",
            "text parc. č. 13/3,": "13/3",
            "text parc.č. 15 text": "15",
            "text parc.č. 15/5 text": "15/5",
        }

        for c, r in cases.items():
            self.assertIsNotNone(PARCEL_NUM_PATTERN.search(c), c)
            self.assertEqual(PARCEL_NUM_PATTERN.search(c).group("num"), r)

    def test_price(self):
        cases = {
            "text 20,- text": "20",
            "text 133.333,- text": "133.333",
            "text 12 331,32 text": "12 331,32",
            "text parc.č. 15/5 text": "15/5",
        }

        for c, r in cases.items():
            self.assertIsNotNone(PRICE_PATTERN.search(c), c)
            self.assertEqual(PRICE_PATTERN.search(c).group("num"), r)


if __name__ == '__main__':
    unittest.main()
