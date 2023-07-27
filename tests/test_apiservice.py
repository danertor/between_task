import csv
import datetime
import os
import json
import shutil
from unittest.mock import Mock

import pytest
from pathlib import Path

from src.Services.ApiService import ApiService
from src.Services.schemas import ApiServiceRow

TMP_FOLDER = str(Path('tests/tmp'))


@pytest.fixture
def tmp_folder() -> None:
    os.makedirs(TMP_FOLDER, exist_ok=True)
    if not os.path.exists(TMP_FOLDER):
        print(f"Test temp folder {TMP_FOLDER} can not be created, continue running")
    yield
    try:
        shutil.rmtree(TMP_FOLDER)
        print(f"Directory '{TMP_FOLDER}' and its contents deleted successfully.")
    except OSError as e:
        print(f"Error deleting directory '{TMP_FOLDER}': {e}. Continuing")


@pytest.fixture
def mocked_api_response():
    response = Mock()
    with open('tests/data/todo_01.json') as fin:
        data = json.load(fin)
        Mock.json = Mock(return_value=data)
        return response


def test_fetch_api_data(mocker, tmp_folder, mocked_api_response):
    api_service = ApiService(url='http://dummy.local', path='tests/tmp')
    mocker.patch("requests.get", return_value=mocked_api_response)
    rows = api_service.fetch_data()
    assert len(rows) == 200
    assert rows[0].userId == 1
    assert rows[0].id == 1
    assert rows[0].title == "delectus aut autem"
    assert rows[0].completed is False


def test_apiservice_run(mocker, tmp_folder, mocked_api_response):
    from src.Application.App import App

    api_service = ApiService(url='http://dummy.local', path=TMP_FOLDER, override_files=True)
    mocker.patch("requests.get", return_value=mocked_api_response)
    api_service.run()

    # validate files
    files_present = False
    for row in mocked_api_response.json():
        current_date = datetime.date.today().strftime("%Y_%m_%d")
        filename = f"{current_date}_{str(row['id'])}.csv"
        file_path = Path(TMP_FOLDER, filename)
        assert os.path.exists(file_path)
        files_present = True
        with open(file_path, 'r') as fin:
            csv_reader = csv.reader(fin)  # can use pandas for better data validation of csv file
            csv_lines = list(csv_reader)
            assert len(csv_lines) == 2  # first line are field names
            line = csv_lines[1]
            parsed_row = ApiServiceRow.model_validate(row)
            assert parsed_row.userId == int(line[0])
            assert parsed_row.id == int(line[1])
            assert parsed_row.title == line[2]
            assert str(parsed_row.completed) == line[3]
    assert files_present is True, "Test failed, no files were found on test"
