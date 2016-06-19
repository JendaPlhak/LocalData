import asyncio
import boto
import csv
import math, os

from boto.s3.connection import S3Connection

from filechunkio import FileChunkIO

class CsvExporter:

    def __init__(self, filename):
        self.filename = filename
        self.file = open(filename, "w")

        fieldnames = ["type", "estate_id", "number", "price_type", "price",
            "dashboard_id", "edesky_id", "publish_date", "address",
            "latitude", "longitude", "edesky_url", "address_code"]
        dialect = csv.excel
        dialect.quoting = csv.QUOTE_ALL
        self.writer = csv.DictWriter(self.file, fieldnames=fieldnames,
            dialect = dialect)
        self.writer.writeheader()

    @asyncio.coroutine
    def export(self, data):
        for row in data:
            # print(row)
            self.writer.writerow(row)

    def upload_to_S3(self, bucket_name, filename):
        self.file.close()

        s3 = boto.connect_s3()
        bucket = s3.get_bucket(bucket_name)

        mp = bucket.initiate_multipart_upload(filename)
        source_size = os.stat(self.filename).st_size
        chunk_size = 52428800
        chunk_count = int(math.ceil(source_size / float(chunk_size)))

        for i in range(chunk_count):
            offset = chunk_size * i
            bytes = min(chunk_size, source_size - offset)
            with FileChunkIO(self.filename, 'r', offset=offset,
                             bytes=bytes) as fp:
                mp.upload_part_from_file(fp, part_num=i + 1)

        # Finish the upload
        mp.complete_upload()
