import asyncio

from document_parser import parse_document


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

            data = yield from self.loop.run_in_executor(self.executor, parse_document, doc)
            yield from self.exporter.export(data)
