import aiohttp
import asyncio
import concurrent
import urllib.parse

class Scraper:

    def __init__(self, queue):
        self._finised = False
        self.doc_queue = queue

    def _get_query_url(self):
        qdict = {
            "keywords": "pronájem bytu",
            "created_from": "2016-04-04",
            "dashboard_id": "59",
            "order": "score",
            "search_with": "sql",
            "page": "1"
        }
        qstring = urllib.parse.urlencode(qdict)
        return "https://edesky.cz/api/v1/documents?" + qstring

    @asyncio.coroutine
    def _do_query(self):
        try:
            session = aiohttp.ClientSession()
            response = yield from session.get(self._get_query_url())
            assert(response.status == 200)
            text = yield from response.text()
        finally:
            yield from session.close()
            return text

    @asyncio.coroutine
    def start_scraping(self):
        xml_data = yield from self._do_query()
        yield from self._generate_docs(xml_data)

    @asyncio.coroutine
    def _generate_docs(self, xml_data):
        for doc in ["Bagr", "Trol"]:
            yield from self.doc_queue.put(doc)
        # Sent poisonous pill
        yield from self.doc_queue.put(None)
