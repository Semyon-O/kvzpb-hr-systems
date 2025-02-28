import io
from typing import Dict

import csv

class ABSFormatImport:

    def import_file(self, file_path) -> [Dict]:
        return NotImplemented


class ExcelFormatImport(ABSFormatImport):

    def import_file(self, file_path) -> [Dict]:
        ...


class CSVFormatImport(ABSFormatImport):

    def import_file(self, file) -> [Dict]:
        file = file.read()
        file_stream = io.BytesIO(file)
        reader = csv.DictReader(io.TextIOWrapper(file_stream, encoding='utf-8-sig'))
        data = []
        for row in reader:
            data.append(row)
        file_stream.close()
        return data


class ImportContext:

    def __init__(self, import_format: ABSFormatImport):
        self.import_context = import_format


    def import_data_from_file(self, file) -> [Dict]:
        data = self.import_context.import_file(file)
        return data