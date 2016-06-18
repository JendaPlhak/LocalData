import asyncio

class CsvExporter:

    def __init__(self, filename):
        self.file = open(filename, "w")

    @asyncio.coroutine
    def export(self, data):
        print(data)
# prodej/pronajem, c.parc/c.popis, c.desky, price, celkova/za metr
