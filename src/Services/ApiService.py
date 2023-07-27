import csv
import logging
import datetime
import os.path
from collections import defaultdict

import requests
from sys import stderr
from pathlib import Path
from typing import List, Optional

from pydantic import ValidationError

from src.Services.schemas import ApiServiceRow

logger = logging.getLogger(__name__)


APISERVICE_CSV_FIELDNAMES = ['userId', 'id', 'title', 'completed']
APISERVICE_TIMEOUT = 30


class ApiService:
    def __init__(self, url: str, path: str, override_files: bool = False):
        self.url: str = url
        self.persistent_path: str = path
        self.override_files: bool = override_files

    def fetch_data(self) -> List[ApiServiceRow]:
        """
        Connects to external API and gets Todo list
        :return: List of Todo items as they are downloaded from external API.
        """
        logger.debug('Fetching data from the API')
        result: List[ApiServiceRow] = []
        request = requests.get(self.url, timeout=APISERVICE_TIMEOUT)
        json_data = request.json()
        for i, row in enumerate(json_data):
            try:
                result.append(ApiServiceRow.model_validate(row))
            except ValidationError as e:
                logger.error("Failed to parse row number %i from API data. Error %s", i, str(e))
                # should push this row data somewhere else to save failed data for debugging purposes
        logger.debug('Fetched %i rows', len(result))
        return result

    def save_data(self, data: List[ApiServiceRow], path: Optional[str] = None) -> None:
        """
        :param data: list of todo list items
        :param path: path where to save the csv files
        """
        logger.debug('Saving %i data rows into storage path %s', len(data), path)
        if not path:
            path = self.persistent_path
        saved_files = 0
        failed_files = 0
        grouped_data_by_id = self._group_data(data)
        for row in data:
            current_date = datetime.date.today().strftime("%Y_%m_%d")
            filename = f"{current_date}_{str(row.id)}.csv"
            file_path = Path(path, filename)
            try:
                if not self.override_files and os.path.exists(file_path):
                    raise FileExistsError
                with open(file_path, 'w', newline='') as fout:
                    csv_writer = csv.writer(fout)
                    csv_writer.writerow(APISERVICE_CSV_FIELDNAMES)
                    csv_writer.writerow([getattr(row, field) for field in APISERVICE_CSV_FIELDNAMES])
            except Exception as e:
                logger.error("Failed to save %i file at %s. Error %s", row.id, str(file_path), str(e))
                failed_files += 1
                # should push this row data somewhere else to collect later on for debugging purposes
            else:
                saved_files += 1
        logger.debug('Correctly saved files: %i. Failed files: %i', saved_files, failed_files)

    def run(self) -> None:
        # to use a logger instead
        print('Running ApiService', file=stderr)

        data = self.fetch_data()
        self.save_data(data)

    def _group_data(self, data: List[ApiServiceRow]) -> dict[int, List[ApiServiceRow]]:
        """
        It prepares the data to be saves into the CSV file.
        Converts a list of Todo items and groups them by item id. If the Todo list contains two items with the same id,
        it will have an structure like this: {1: [<item_a>, <item_b>]}.
        :param data: list of Todo items
        :return: a dictionary where the item id are keys and the values are a list of items with the same item id
        """
        grouped_data = defaultdict(list)
        for row in data:
            grouped_data[row.id].append(row)
        return grouped_data
