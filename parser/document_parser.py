# we need unicode matching provided by alternative regex library
import regex
from address_utils import AddressValidator
re = regex


# TODO: hledat pronajem
# TODO: name: hledat ZP
# NAME_PATTERN = re.compile(r'(záměru? prodeje|ZP )', re.IGNORECASE)
NAME_PATTERN = re.compile(r'záměru? prodeje', re.IGNORECASE)

HOUSE_NUM_PATTERN = re.compile(r'č\.? ?p\. (?P<num>[0-9]+)', re.IGNORECASE)
PARCEL_NUM_PATTERN = re.compile(r'parc\. ?č\. (?P<num>[0-9]+/?[0-9]*)', re.IGNORECASE)

BASE_ADDRESS_PATTERN = re.compile(r'(.{0,20}\s\p{Lu}\p{Ll}+)', re.U)
ADDRESS_PATTERN = re.compile(r'([ ,]?)(?P<street>'
                                r'(U |Na |Pod |náměstí |nám |nám. )?'
                                r'(\p{Lu}\p{Ll}{3,})( \p{Lu}\p{Ll}{3,})?'
                                r'( \p{Ll}{3,})?'
                             r')'
                             r' (?P<num>\d+(?:/\d+)?)', re.U)

# PRICE_PATTERN = re.compile(r'(?P<price>\d[\. \d]*),(?:\-|\d{2})')
# PRICE_PATTERN = re.compile(r'(?P<price>\d[\. \d]*)(?:[,\.]\-|[,\.]\d{2}| Kč)')
# PRICE_PATTERN = re.compile(r'(?<=(\D|^))(?P<price>\d{1,3}(?:[\. ]\d{3})*)([,\.]\-|[,\.]\d{2}| Kč)')
PRICE_PATTERN = re.compile(
    r'(\D|^)(?P<price>\d+|(\d{1,3}(?:[\. ]\d{3})*))([,\.]\-|[,\.]\d{2}(?=\s)| Kč)(?P<type>(?:\/|1)(?:(m|rn)2))?')


def parse_document(data):
    res = {
        "dashboard_id": data["dashboard_id"],
        "edesky_id": data["edesky_id"],
        "edesky_url": data["edesky_url"],
        "publish_date": data["publish_date"],
        "type": "sale"
    }

    doc_text = data['doc_name']
    doc_content = data['doc_text_content']

    name_sale = NAME_PATTERN.search(doc_text)
    if not name_sale:
        return []

    location = None
    print(ADDRESS_PATTERN.findall(doc_content))
    for address in ADDRESS_PATTERN.finditer(doc_content):
        if address.group("street") == "Praha":
            continue

        location = validate_address(address.group("street"), address.group("num"))

        if location:
            break

    if location is None:
        return []

    res['address_street'] = address.group("street")
    res['address_num'] = address.group("num")
    res['latitude'] = location[0][0]
    res['longitude'] = location[0][1]
    res['address_code'] = location[1]

    parcel_num = HOUSE_NUM_PATTERN.search(doc_content)
    if parcel_num:
        res["estate_id"] = "parcel_number"
        res["number"] = parcel_num.group("num")

    house_num = HOUSE_NUM_PATTERN.search(doc_content)
    if house_num:
        res["estate_id"] = "house_number"
        res["number"] = house_num.group("num")

    price = PRICE_PATTERN.search(doc_content)
    if price:
        res["price"] = price.group("price")
        res["price_type"] = "per_meter" if price.group("type") else "total"

    return [res]


def validate_address(street, number):

    split = number.split("/")
    lat_lon = None

    if (len(split) == 1):
        a = AddressValidator(street, house_num=number)
        lat_lon = a.get_location()

        if lat_lon is None:
            a = AddressValidator(street, descr_num=number)
            lat_lon = a.get_location()
    else:
        a = AddressValidator(street, descr_num=split[0], house_num=split[1])
        lat_lon = a.get_location()

    return lat_lon
