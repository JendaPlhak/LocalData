import asyncio
import concurrent

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
