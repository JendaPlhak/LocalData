import asyncio


class Parser:
    def __init__(self, loop, executor, doc_queue, exporter):
        self.loop = loop
        self.executor = executor
        self.doc_queue = doc_queue
        self.exporter = exporter

    @asyncio.coroutine
    def start_processing(self):
        while True:
            doc = yield from self.doc_queue.get()
            # Poisonous pill means the work is done.
            if doc is None:
                break
            data = yield from self.loop.run_in_executor(self.executor,
                    parse_document, doc)
            yield from self.exporter.export(data)

def parse_document(data):
    return "WEEEE"
