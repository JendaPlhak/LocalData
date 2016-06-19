import copy
import random

import geocoder
import os
import pandas as pd
import pickle
import redis


# vyheldat kandidaty v textu
# zkusit match na tabulce adresnich mist (ulic)
# posledni resort zkusit


class AddressValidator:

    ADDRESS_TABLE_FILE = os.path.join(os.path.dirname(__file__), os.path.pardir, 'datasets/adresni_mista_wgs84_praha.csv')

    # TODO: gogole accuracy: ROOFTOP
    GEOCODERS = [
        ('google', None, None, None),
        # ('google', None, 'accuracy', ['ROOFTOP']),
        # ('google', None, 'types', ['street_address']),
        # ('mapquest', 'OfSOmTltOxOz7eu5WIvXGFFusOOKERIK', None, None),
        # ('osm', None, None, None)
        # 'here'
    ]

    def __init__(self, street, descr_num=None, house_num=None, city='Prague', country='CZ'):
        self.street = street
        self.descr_num = float(descr_num) if descr_num else None
        self.house_num = int(house_num) if house_num else None
        self.city = city
        self.country = country

        self.accuracy = None
        self.source = None

        self.r = redis.StrictRedis(host='localhost', port=6379, db=1)

    def _get_address_line(self):
        line = self.street

        if self.descr_num and self.house_num:
            line = "%s %s/%s" % (line, int(self.descr_num), int(self.house_num))
        elif self.descr_num:
            line = "%s %s" % (line, int(self.descr_num))
        elif self.house_num:
            line = "%s %s" % (line, int(self.house_num))

        return "%s, %s, %s" % (line, self.city, self.country)

    def load_table(self):
        data = pd.read_csv(self.ADDRESS_TABLE_FILE, encoding="utf-8", sep=",")
        # TODO: index
        # data = data.set_index(["Název ulice", "Číslo domovní", "Číslo orientační"])

        return data

    # TODO: search by orient_num or house_num
    def step_table(self):
        data = self.load_table()
        # query = (lambda df: ((df["Název ulice"] == self.street) & (df["Číslo orientační"] == self.orent_num)))

        if self.house_num:
            comparator = (data["Název ulice"] == self.street) & (
                (data["Číslo domovní"] == self.descr_num) | (data["Číslo orientační"] == float(self.house_num))
            )
        else:
            comparator = (data["Název ulice"] == self.street) & (data["Číslo domovní"] == self.descr_num)

        res = data[(comparator)]

        if res.empty:
            return None

        res = res.iloc[0]

        self.source = 'table'
        # X=lon, Y=lat in dataset
        return res["Y"], res["X"]

    def step_geocoding(self):
        res = None

        geocoders = copy.deepcopy(self.GEOCODERS)
        random.shuffle(geocoders)

        for gc in geocoders:
            gc, key, accuracy, allowed_accuracy = gc
            args = [gc]
            kwargs = {}
            if key:
                kwargs["key"] = key

            res = getattr(geocoder, gc)(*args, **kwargs)

            if res:
                if self.accuracy and allowed_accuracy:
                    self.accuracy = getattr(res, accuracy, None) if accuracy else None
                    if self.accuracy not in allowed_accuracy:
                        return None

                self.source = gc
                return res.latlng

        return res

    def lat_lon(self):
        # cache
        res = self.r.get(self._get_address_line())
        if res:
            self.source = 'cache'
            return pickle.loads(res)

        # table
        res = self.step_table()
        if res:
            self.r.set(self._get_address_line(), pickle.dumps(res))
            return res

        # geocoders
        res = self.step_geocoding()
        if res:
            self.r.set(self._get_address_line(), pickle.dumps(res))
            return res

        return None


if __name__ == '__main__':
    a = AddressValidator("Bělehradská", descr_num="660", house_num="85")
    # a = AddressValidator("Vodičkova", descr_num="18")
    print("Q:", a._get_address_line())
    print("A:", a.lat_lon(), a.source, a.accuracy)
