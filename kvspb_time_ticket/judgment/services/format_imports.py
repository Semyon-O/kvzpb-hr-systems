import io
import re
from typing import Dict
import pandas as pd
import csv

class ABSFormatImport:

    def import_file(self, file_path) -> [Dict]:
        return NotImplemented


class ExcelFormatImport(ABSFormatImport):

    def import_file(self, file_path) -> [Dict]:
        job_places = []
        data = pd.read_excel(file_path)
        for job_place in data.values:
            place = self.__extract_number(job_place[0])
            job = job_place[1]
            print(job, place)
            job_places.append(
                {
                    "номер участка": str(place),
                    "должность": job
                }
            )
        return job_places


        return job_places
    def __extract_number(self, text):
        """
        Извлекает число из строки, содержащей номер в форматах:
        - "№12" → 12
        - "№ 12" → 12
        - "12" → 12
        - "№     12" → 12
        - "Number 12" → 12 (если есть другие символы)

        Возвращает:
        - int, если число найдено
        - None, если число не найдено
        """

        match = re.search(r'\d+', str(text))
        if match:
            return int(match.group())
        return None  # или можно вернуть 0, если нужно число по умолчанию

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