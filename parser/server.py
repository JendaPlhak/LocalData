import asyncio
import concurrent

from scraper import Scraper
from parser import Parser
from exporter import CsvExporter

@asyncio.coroutine
def generate_data(loop, executor):
    doc_queue = asyncio.Queue(10)
    scraper = Scraper(doc_queue)
    exporter = CsvExporter("export.csv")
    parser = Parser(loop, executor, doc_queue, exporter)

    try:
        scraper_task = loop.create_task(scraper.start_scraping())
        parser_task = loop.create_task(parser.start_processing())
        yield from asyncio.gather(scraper_task, parser_task, loop = loop)
    except asyncio.CancelledError:
            pass
    finally:
        scraper_task.cancel()


if __name__ == '__main__':

    thread_pool_size = 2

    loop = asyncio.get_event_loop()
    executor = concurrent.futures.ProcessPoolExecutor(thread_pool_size)
    loop.set_debug(True)

    run_task = loop.create_task(generate_data(loop, executor))
    try:
        loop.run_until_complete(run_task)
    except KeyboardInterrupt as e:
        run_task.cancel()

    executor.shutdown()