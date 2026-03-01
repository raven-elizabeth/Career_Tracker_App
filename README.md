# Career Tracker App
## Introduction
The Career Tracker App is a web app designed to help users track their career progress, set goals
and manage their professional development. 
The app provides tracking of daily activities, enabling users to keep a record and stay on track.

### TARGET AUDIENCE
The app is ideal for all professionals who want to monitor their career growth,
although it is particularly designed with apprentices and those in their early career in mind.

___

## To run the app:

1. Clone the repository
2. Install the required dependencies using `pip install -r requirements.txt`
3. Run the Flask api using `python -m api.api` (keep it running - without this the app WILL NOT WORK)
4. Run the main app in a separate terminal by using `python main.py`

___

## Endpoints

<br>

GET: `http://127.0.0.1:5000/api/csv/entries/<date>`

Gets the entry for the specified date. 

If no entry exists, it returns a message indicating that no entry was found rather than raising. 
``` 
200: Entry found and returned successfully.
404: No entry found for the specified date.
503: Server error; file unavailable. 
```

DELETE: `http://127.0.0.1:5000/api/csv/entries/<date>`

Deletes the entry for the specified date. Raises an error if no entry exists for that date.
```
204 - Entry deleted successfully.
404 - No entry found for the specified date.
503 - Server error; file unavailable.
```

<br>

### Following endpoints require JSON body with the date and at least one field value:

<br>

POST: `http://127.0.0.1:5000/api/csv/entries`

Saves a new entry for the specified date. Raises an error if entry already exists for that date.
```
201 - Entry created successfully.
400 - Bad request; missing required fields or invalid data format.
409 - Conflict; entry already exists for the specified date.
```

PUT: `http://127.0.0.1:5000/api/csv/entries/<date>`

Replaces the entry for the specified date with the new data provided. 
Raises an error if no entry exists for that date.
```
200 - Entry updated successfully.
400 - Bad request; missing required fields or invalid data format.
404 - No entry found for the specified date.
503 - Server error; file unavailable.
```

PATCH: `http://127.0.0.1:5000/api/csv/entries/<date>`

Partially updates the entry for the specified date with the new data provided.
Raises an error if no entry exists for that date.
```
200 - Entry updated successfully.
400 - Bad request; missing required fields or invalid data format.
404 - No entry found for the specified date.
503 - Server error; file unavailable.
```
___

## Libraries & Tools Used

### Language
- **Python** — The programming language used for both the API and GUI.

### API
- **Flask** — Micro web framework used to build and serve the REST API (`api/api.py`). Chosen for its simplicity and familiarity.
- **Requests** — HTTP client library used by the API client (`data_access/api_client/client.py`) to make GET, POST, PUT, PATCH, and DELETE requests to the Flask API.

### GUI
- **Tkinter** — Python's built-in GUI library, used to build all screens (`gui/`). Chosen for its availability as a standard library with no extra install required.
- **Tkcalendar** — Third-party calendar widget for Tkinter, used in the search and new entry screens to allow date selection.

### Data
- **Pandas** — Data manipulation library used in the CSV repository (`data_access/repositories/csv_database_repository.py`) for reading, writing, and indexing CSV data. Date indexing provides O(1) lookups.
- **CSV** — File format used for persistent data storage (`data/entries.csv`). Chosen for simplicity; no database server setup required.

### Testing
- **unittest** — Python's built-in testing framework, used to write all tests across `tests/`.
- **pytest** — Used as the test runner (e.g. by PyCharm). Tests are written in `unittest` style but discovered and run by pytest.
- **unittest.mock** — Used in `client_test.py` to mock HTTP responses from the API without needing a running server.

### Logging
- **logging** — Python's built-in logging module, configured in `logs/logging_config.py` and used across the API, repository, and client for debug, info, warning, and error logs.

### Project Management & Version Control
- **Jira** — Used to track epics and tasks during development.
- **GitHub** — Used for version control and to host the repository.

___

### Dependencies
The following are transitive dependencies installed automatically with the above libraries.
They are pinned in `requirements.txt` for reproducibility but are not used directly in the codebase:

| Library | Transitive Dependencies |
| --- | --- |
| Flask | werkzeug, jinja2, markupsafe, itsdangerous, blinker, click, colorama |
| requests | certifi, charset-normalizer, idna, urllib3 |
| pandas | numpy, python-dateutil, tzdata, six |
| tkcalendar | babel |
| pytest | colorama, iniconfig, packaging, pluggy, pygments |

___
## Running Tests
Tests are written using Python's built-in `unittest` framework. `pytest` is included as a dependency 
as it is used as the test runner (e.g. by PyCharm, which I used). There are three ways to run them:

- **Run all tests at once** from the project root:
  ```
  python -m unittest discover -s tests -p "*_test.py" --top-level-dir .
  ```

- **Run a specific test file** from the project root:
  ```
  python -m unittest tests.api_tests.api_test
  python -m unittest tests.api_tests.client_test
  python -m unittest tests.database_tests.csv_database_repository_test
  python -m unittest tests.domain_tests.entry_test
  ```

- **Run a test file directly** (e.g. in an IDE or from its own directory):
  Each test file can be run directly as a script, e.g. `python api_test.py`
___

## Examples of Use
...

___

## Future Improvements
In the future, I would consider implementing more features, such as **goal setting**, **progress visualization**,
and a **to-do list**. I could also explore **integrating** with other platforms (e.g., LinkedIn) to automatically 
track career milestones and achievements.
If I want to tailor the app more towards apprentices, I could consider features such as a **KSB tracker**
and **portfolio evidence storage**, along with reminders to keep these updated and other apprentice resources.

I would like to add more **accessibility features** to the app, such as **keyboard navigation**, 
**complete screen reader support**, and an **accessibility tool menu**
to allow users to easily adjust the app's settings to suit their needs. 
I would also like to make the designs **responsive** for different screen sizes.

- I chose to use **Flask** for the API because I am familiar with it, and it is lightweight.

- I chose to use **Tkinter** for the GUI because it is a built-in library in **Python** and allows for 
quick development of a simple user interface.
I would consider implementing a **React** frontend, however, I am unfamiliar with it, so this would have a 
steep learning curve and would require more time than I had available for this project.


- I chose to use a **CSV file** for data storage in this project for simplicity and ease of implementation.
I would consider implementing a proper database, however I am most familiar with **SQL & MySQL** and this would have 
required the assignment marker to set up a MySQL database for the project.
I did consider **SQLite**, which does not require a separate server, but I am have not used it before,
so it would have required additional time to learn and implement.
___

## Additional Notes
See the documentation folder for further supporting materials, 
including the SRS document, statement on AI use, accompanying project poster, 
and any other relevant files/diagrams.
