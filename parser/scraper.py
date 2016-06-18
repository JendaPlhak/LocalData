import aiohttp
import asyncio
import concurrent
import urllib.parse
from pyquery import PyQuery as pq


class Scraper:
    def __init__(self, queue):
        self._finised = False
        self.doc_queue = queue

    # TODO: iterate through parameters, pages
    def _get_query_url(self):
        qdict = {
            "keywords": "prodej",
            "created_from": "2016-05-04",
            "dashboard_id": "59",
            "order": "score",
            "search_with": "es",
            "page": "1"
        }
        qstring = urllib.parse.urlencode(qdict)
        return "https://edesky.cz/api/v1/documents?" + qstring

    @asyncio.coroutine
    def _do_query(self):
        try:
            session = aiohttp.ClientSession()
            response = yield from session.get(self._get_query_url())
            assert (response.status == 200)
            text = yield from response.text()
        finally:
            yield from session.close()
            return text

    @asyncio.coroutine
    def start_scraping(self):
        xml_data = yield from self._do_query()
        yield from self._generate_docs(xml_data)

    @asyncio.coroutine
    def _get_txt_doc_content(self, doc_text_url):
        try:
            session = aiohttp.ClientSession()
            response = yield from session.get(doc_text_url)
            assert (response.status == 200)
            text = yield from response.text()
        finally:
            yield from session.close()
            return text

    @asyncio.coroutine
    def _generate_docs(self, xml_data):

        src = pq(xml_data.encode('utf-8'))

        for doc in src("document"):
            doc_text_content = yield from self._get_txt_doc_content(doc.attrib.get("edesky_text_url"))

            doc = {
                "doc_name": doc.attrib.get("name"),
                "doc_text_url": doc.attrib.get("edesky_text_url"),
                "doc_orig_url": doc.attrib.get("orig_url"),
                "doc_text_content": doc_text_content
            }

            yield from self.doc_queue.put(doc)

        # Sent poisonous pill
        yield from self.doc_queue.put(None)
