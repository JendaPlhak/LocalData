import unittest

from document_parser import HOUSE_NUM_PATTERN, PARCEL_NUM_PATTERN, PRICE_PATTERN, ADDRESS_PATTERN


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

    # def test_price(self):
    #     cases = {
    #         "text 20,- text": "20",
    #         "text 133.333,- text": "133.333",
    #         "text 12 331,32 text": "12 331,32",
    #         "text parc.č. 15/5 text": "15/5",
    #     }
    #
    #     for c, r in cases.items():
    #         self.assertIsNotNone(PRICE_PATTERN.search(c), c)
    #         self.assertEqual(PRICE_PATTERN.search(c).group("num"), r)

    def test_address(self):
        cases = {
            "Jugoslavska 181": ("Jugoslavska", "181"),
            "Jugoslávská 181": ("Jugoslávská", "181"),
            "adrese Jugoslávská 181/17, a to": ("Jugoslávská", "181/17"),
            "adrese U Lesa 17, a to": ("U Lesa", "17"),
            "adrese U Milosrdných bratří 17, a to": ("U Milosrdných bratří", "17"),
            "adrese U Bratří 17, a to": ("U Bratří", "17"),
            "adrese náměstí Míru 17, a to": ("náměstí Míru", "17"),
            # "adrese Praha 1 a to": None,
            "adrese U bratří 17, a to": None,
            "adrese bratří 17, a to": None,
            "adrese A 1 a to": None,
            "čj. UMCPl 093202/2016": None,
            "Kč za 1 m2": None,
        }

        for c, r in cases.items():

            res = ADDRESS_PATTERN.search(c)

            if r:
                if c is None:
                    self.assertIsNone(res, c)
                else:
                    s, n = r
                    self.assertIsNotNone(res, c)
                    self.assertEqual(res.group("street"), s)
                    self.assertEqual(res.group("num"), n)


if __name__ == '__main__':
    unittest.main()
