import re


# TODO: hledat pronajem
# TODO: name: hledat ZP
# NAME_PATTERN = re.compile(r'(záměru? prodeje|ZP )', re.IGNORECASE)
NAME_PATTERN = re.compile(r'záměru? prodeje', re.IGNORECASE)

HOUSE_NUM_PATTERN = re.compile(r'č\.? ?p\. (?P<num>[0-9]+)', re.IGNORECASE)
PARCEL_NUM_PATTERN = re.compile(r'parc\. ?č\. (?P<num>[0-9]+/?[0-9]*)', re.IGNORECASE)

# PRICE_PATTERN = re.compile(r'(?P<price>\d[\. \d]*),(?:\-|\d{2})')
# PRICE_PATTERN = re.compile(r'(?P<price>\d[\. \d]*)(?:[,\.]\-|[,\.]\d{2}| Kč)')
# PRICE_PATTERN = re.compile(r'(?<=(\D|^))(?P<price>\d{1,3}(?:[\. ]\d{3})*)([,\.]\-|[,\.]\d{2}| Kč)')
PRICE_PATTERN = re.compile(
    r'(\D|^)(?P<price>\d+|(\d{1,3}(?:[\. ]\d{3})*))([,\.]\-|[,\.]\d{2}(?=\s)| Kč)(?P<type>(?:\/|1)(?:(m|rn)2))?')


def parse_document(data):
    res = {
        "dashboard_id": data["dashboard_id"],
        "edesky_id": data["edesky_id"],
        "publish_date": data["publish_date"],
        "type": "sale"
    }

    doc_text = data['doc_name']
    doc_content = data['doc_text_content']

    name_sale = NAME_PATTERN.search(doc_text)
    if not name_sale:
        return []

    parcel_num = HOUSE_NUM_PATTERN.search(doc_content)
    if parcel_num:
        res["estate_id"] = "parcel_number"
        res["number"] = parcel_num.group("num")
    else:
        house_num = HOUSE_NUM_PATTERN.search(doc_content)
        if house_num:
            res["estate_id"] = "house_number"
            res["number"] = house_num.group("num")
        else:
            return []

    price = PRICE_PATTERN.search(doc_content)
    if price:
        res["price"] = price.group("price")
        res["price_type"] = "per_meter" if price.group("type") else "total"
    else:
        return []

    return [res]


#
# if __name__ == '__main__':
#     documents = []
#     for d in documents:
