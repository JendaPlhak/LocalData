import aiohttp
import asyncio
import concurrent
import time
from elasticsearch import Elasticsearch

class ElasticScraper:

    def __init__(self, loop, queue):
        self.loop = loop
        self.doc_queue = queue

    def get_query(self):
        search_text = "prodej"
        from_date = "2016-04-18T21:12:41.028+02:00"
        return {
            "size": 20000,
            "query": {
                "filtered": {
                    "query": {
                        "query_string": {
                            "default_operator": 'AND',
                            "query": search_text
                        }
                    },
                    "filter": {
                        "bool": {
                            "must": [
                                {
                                    "range":{
                                        "created_at":{
                                            "from": from_date,
                                            "include_lower": False
                                        }
                                    }
                                }
                            ]
                        }
                    }
                }
            }
        }

    @asyncio.coroutine
    def start_scraping(self):
        es = Elasticsearch(['localhost', '10.0.3.248'])
        result = es.search(index="documents_production", body=self.get_query())

        for hit in result['hits']['hits']:
            yield from self._process_doc(hit)
        yield from self.doc_queue.put(None)

    @asyncio.coroutine
    def _process_doc(self, hit):
        doc_with_text = {
            "dashboard_id": hit["_source"]["dashboard_id"],
            "doc_name": hit["_source"]["name"],
            "edesky_id": hit["_id"],
            "doc_text_url": "",
            "doc_orig_url": "",
            "doc_text_content": hit["_source"]["attachments_content"]
        }
        yield from self.doc_queue.put(doc_with_text)




