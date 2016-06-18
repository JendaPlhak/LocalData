import asyncio
import concurrent

from scraper import Scraper
from parser import Parser

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
