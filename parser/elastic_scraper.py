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
        search_text = "prodej~"
        from_date = "2016-01-01"
        return {
            "size": 500000,
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
                                    "range": {
                                        "created_at":{
                                            "from": from_date,
                                            "include_lower": False
                                        }
                                    }
                                },
                                {
                                    "terms": {
                                        "dashboard_id": [
                                            109, 110, 115, 116, 117, 118, 119, 120, 121, 138, 143, 159, 166, 167, 168,
                                            169, 170, 171, 172, 173, 174, 175, 176, 196, 864, 865, 866, 867, 868, 869,
                                            870, 871, 872, 873, 874, 875, 876, 877, 878, 879, 880, 881, 882, 883, 884,
                                            885, 886, 887, 888, 889, 890, 891, 892, 893, 894, 895,
                                        ]
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

        print('=== ES # of hits:', result['hits']['total'])

        for hit in result['hits']['hits']:
            yield from self._process_doc(hit)
        yield from self.doc_queue.put(None)

    @asyncio.coroutine
    def _process_doc(self, hit):
        doc_with_text = {
            "dashboard_id": hit["_source"]["dashboard_id"],
            "doc_name": hit["_source"]["name"],
            "edesky_id": hit["_id"],
            "doc_text_content": hit["_source"]["attachments_content"],
            "publish_date": hit["_source"]["created_at"][0:10]
        }
        yield from self.doc_queue.put(doc_with_text)




