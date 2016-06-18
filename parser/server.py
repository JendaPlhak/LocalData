import aiohttp
import asyncio
import concurrent
import urllib.parse
import xml.etree.ElementTree as ET


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

class Parser:
    def __init__(self, doc_queue):
        self.doc_queue = doc_queue

    @asyncio.coroutine
    def start_processing(self):
        while True:
            doc = yield from self.doc_queue.get()
            # Poisonous pill means the work is done.
            if doc is None:
                break
            print(doc)


@asyncio.coroutine
def generate_data(loop):
    doc_queue = asyncio.Queue(10)
    scraper = Scraper(doc_queue)
    parser = Parser(doc_queue)

    try:
        scraper_task = loop.create_task(scraper.start_scraping())
        parser_task = loop.create_task(parser.start_processing())
        yield from asyncio.gather(scraper_task, loop = loop)
    except CancelledError:
            pass
    finally:
        scraper_task.cancel()


if __name__ == '__main__':

    thread_pool_size = 8

    loop = asyncio.get_event_loop()
    executor = concurrent.futures.ThreadPoolExecutor(thread_pool_size)
    loop.set_debug(True)

    run_task = loop.create_task(generate_data(loop))
    try:
        loop.run_until_complete(run_task)
    except KeyboardInterrupt as e:
        listen_task.cancel()
