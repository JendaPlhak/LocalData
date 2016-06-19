import asyncio
import argparse
import concurrent

from web_scraper import WebScraper
from elastic_scraper import ElasticScraper
from parser import Parser
from exporter import CsvExporter
from datetime import datetime


thread_pool_size = 4

@asyncio.coroutine
def generate_data(args, loop, executor):
    doc_queue = asyncio.Queue()

    if args.web_scraper:
        scraper = WebScraper(loop, doc_queue)
    else:
        scraper = ElasticScraper(loop, doc_queue)

    exporter = CsvExporter("export.csv")
    parser = Parser(loop, executor, doc_queue, exporter,
        thread_pool_size)

    try:
        scraper_task = loop.create_task(scraper.start_scraping())
        parser_task = loop.create_task(parser.start_processing())
        yield from asyncio.gather(scraper_task, parser_task, loop = loop)
    except asyncio.CancelledError:
            pass
    finally:
        scraper_task.cancel()
        parser_task.cancel()

    path = "data/price_data_{0:%Y-%m-%d_%H-%M-%S}".format(datetime.now())
    # exporter.upload_to_S3("cz-whatthehack-local-information", path)

def get_args():
    p = argparse.ArgumentParser()
    p.add_argument("-w", "--web_scraper", help="Use WebScraper",
        action="store_true")
    p.add_argument("-e", "--elastic_scraper", help="Use ElasticScraper",
        action="store_true")

    return p.parse_args()


if __name__ == '__main__':

    args = get_args()

    loop = asyncio.get_event_loop()
    executor = concurrent.futures.ProcessPoolExecutor(thread_pool_size)
    loop.set_debug(True)

    run_task = loop.create_task(generate_data(args, loop, executor))
    try:
        loop.run_until_complete(run_task)
    except KeyboardInterrupt as e:
        run_task.cancel()

    executor.shutdown()
