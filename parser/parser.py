import asyncio
import re
import time


class Parser:
    def __init__(self, loop, executor, doc_queue, exporter, paralel_requests):
        self.loop = loop
        self.executor = executor
        self.doc_queue = doc_queue
        self.exporter = exporter
        self.paralel_requests = paralel_requests

    @asyncio.coroutine
    def start_processing(self):
        tasks = [self.loop.create_task(self._process_documents())
            for _ in range(self.paralel_requests)]
        try:
            yield from asyncio.gather(*tasks, loop = self.loop)
        except asyncio.CancelledError:
                pass
        finally:
            for task in tasks:
                task.cancel()
            yield from asyncio.wait(tasks)

    @asyncio.coroutine
    def _process_documents(self):
        while True:
            doc = yield from self.doc_queue.get()
            # Poisonous pill means the work is done.
            if doc is None:
                yield from self.doc_queue.put(None)
                break

            data = yield from self.loop.run_in_executor(self.executor,
                    parse_document, doc)
            yield from self.exporter.export(data)


# TODO: hledat pronajem
# TODO: name: hledat ZP
# NAME_PATTERN = re.compile(r'(záměru? prodeje|ZP )', re.IGNORECASE)
NAME_PATTERN = re.compile(r'záměru? prodeje', re.IGNORECASE)

HOUSE_NUM_PATTERN = re.compile(r'č\.? ?p\. (?P<num>[0-9]+)', re.IGNORECASE)
PARCEL_NUM_PATTERN = re.compile(r'parc\. ?č\. (?P<num>[0-9]+/?[0-9]*)', re.IGNORECASE)

# PRICE_PATTERN = re.compile(r'(?P<price>\d[\. \d]*),(?:\-|\d{2})')
# PRICE_PATTERN = re.compile(r'(?P<price>\d[\. \d]*)(?:[,\.]\-|[,\.]\d{2}| Kč)')
# PRICE_PATTERN = re.compile(r'(?<=(\D|^))(?P<price>\d{1,3}(?:[\. ]\d{3})*)([,\.]\-|[,\.]\d{2}| Kč)')
PRICE_PATTERN = re.compile(r'(\D|^)(?P<price>\d+|(\d{1,3}(?:[\. ]\d{3})*))([,\.]\-|[,\.]\d{2}(?=\s)| Kč)(?P<type>(?:\/|1)(?:(m|rn)2))?')


def parse_document(data):
    res = {
        "dashboard_id": data["dashboard_id"]
    }

    doc_text = data['doc_name']
    doc_content = data['doc_text_content']

    name_sale = NAME_PATTERN.search(doc_text)
    if not name_sale:
        return []

    res["type"] = "sale"

    house_num = HOUSE_NUM_PATTERN.search(doc_content)
    if house_num:
        res["estate_id"] = "house_number"
        res["number"] = house_num.group("num")
    else:
        parcel_num = HOUSE_NUM_PATTERN.search(doc_content)
        if parcel_num:
            res["estate_id"] = "parcel_number"
            res["number"] = parcel_num.group("num")

    price = PRICE_PATTERN.search(doc_content)
    if price:
        res["price"] = price.group("price")
        res["price_type"] = "per_meter" if price.group("type") else "total"
    return [res]

#
# if __name__ == '__main__':
#     documents = []
#     for d in documents:
