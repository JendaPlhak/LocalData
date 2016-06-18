import aiohttp
import asyncio
import concurrent
import urllib.parse
import time
from pyquery import PyQuery as pq


class Scraper:
    def __init__(self, loop, queue):
        self.loop = loop
        self.doc_queue = queue

    # TODO: iterate through parameters, pages
    def _get_query_url(self, page):
        qdict = {
            "keywords": "Kč?m2",
            "created_from": "2016-01-01",
            # "dashboard_id": "59",
            "order": "date",
            "search_with": "es",
            "page": page
        }
        qstring = urllib.parse.urlencode(qdict)
        return "https://edesky.cz/api/v1/documents?" + qstring

    @asyncio.coroutine
    def _do_query(self, page):
        try:
            session = aiohttp.ClientSession()
            print(self._get_query_url(page))
            response = yield from session.get(self._get_query_url(page))
            assert (response.status == 200)
            text = yield from response.text()
        finally:
            yield from session.close()
            return text

    @asyncio.coroutine
    def start_scraping(self):
        page = 1
        pages_total = 1

        while page <= pages_total:
            print("---------------------Scraping page %d" % page)
            xml_data = yield from self._do_query(page)
            yield from self._generate_docs(xml_data)

            pages_total = self._get_total_pages(xml_data)
            page += 1

        # Sent poisonous pill
        yield from self.doc_queue.put(None)

    def _get_total_pages(self, xml_data):
        src = pq(xml_data.encode('utf-8'))
        return int(src("page")[0].attrib.get("total"))


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
    def _generate_doc(self, doc):
        url = doc.attrib.get("edesky_text_url")
        doc_text_content = yield from self._get_txt_doc_content(url)

        doc_with_text = {
            "dashboard_id": doc.attrib.get("dashboard_id"),
            "edesky_id": doc.attrib.get("edesky_id"),
            "doc_name": doc.attrib.get("name"),
            "doc_text_url": doc.attrib.get("edesky_text_url"),
            "doc_orig_url": doc.attrib.get("orig_url"),
            "doc_text_content": doc_text_content
        }
        yield from self.doc_queue.put(doc_with_text)

    @asyncio.coroutine
    def _generate_docs(self, xml_data):

        src = pq(xml_data.encode('utf-8'))

        tasks = []
        for doc in src("document"):
            task = self.loop.create_task(self._generate_doc(doc))
            tasks.append(task)

        try:
            yield from asyncio.gather(*tasks, loop = self.loop)
        except asyncio.CancelledError:
                pass
        finally:
            for task in tasks:
                task.cancel()
            yield from asyncio.wait(tasks)


