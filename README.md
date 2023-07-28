# Python App Exercise

## Hot to run:
 - Needs python +3.9
 - `pip install -r requirements.txt`
 - `python main.py`

## Tests:
 - `pytest tests`

## Assumptions
Currently, the external API is producing todo items with unique `id` values, so one single CSV file is created for every entry on the downloaded json data.

The software is capable of appending multiple Todo items as records to a single CSV if they share the same `id` value. But as said before it is not the case as for now because of how the data produced by the external API.


## Tech debt:
 - This service should operate on an asynchronous matter to dramatically increase the performance. The current code will block the python interpreter when calling the external API or when saving data into the storage. The async client of `httpx` package can be use for calling the external API and `asyncIO` can be used for saving data into local storage. 
 - Create unittest and integration tests separately in tests
 - Create a Storage class for saving the files.
 - Use a super class or interface for ApiService that controls the connection and retry methods to external APIs. Maybe the storage.save()
 - Use a pre-commit package: pylint, flake8,...
 - Use Github Pull-Requests requisites steps pre-merge
 - Improve linter warnings. "ApiService" not snake case, and so on
 - Use flake8 instead of pylint as linter
 - Create unit test for when overriding files yes or not
 - Create tests for when API fails.

## Exercise
- Use the ApiService to fetch TODOs from an API and save them into the _storage_ folder
    - TODOs can be accessed from this URL: https://jsonplaceholder.typicode.com/todos/
    - Each TODO should be saved on a single file in CSV format
    - The filename must contain the TODO "id" prefixed with the current date.
        - Example: 2021_04_28_123.csv


## Extra points
- Use _requests_ library from [PyPI](https://pypi.org/project/requests/)
