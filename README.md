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
3. Run the Flask api using `python -m api.api` (keep it running)
4. Run the main app in a separate terminal by using `python main.py`

___

## Endpoints
GET: `http://127.0.0.1:5000/api/csv/entries/<date>`

Gets the entry for the specified date. 
If no entry exists, it returns a message indicating that no entry was found.

DELETE: `http://127.0.0.1:5000/api/csv/entries/<date>`

Deletes the entry for the specified date. Raises an error if no entry exists for that date.

<br>

Following endpoints require JSON body with the date and at least one field value:

POST: `http://127.0.0.1:5000/api/csv/entries`

Saves a new entry for the specified date. Raises an error if ...

PUT: `http://127.0.0.1:5000/api/csv/entries/<date>`

Replaces the entry for the specified date with the new data provided. 
Raises an error if no entry exists for that date.

PATCH: `http://127.0.0.1:5000/api/csv/entries/<date>`

Partially updates the entry for the specified date with the new data provided.
Raises an error if no entry exists for that date.

___

## Libraries & Tools Used
- Python
  - The programming language used for both the API and the main app.
- Jira
  - A project management tool used to track epics and tasks for the app development process.
- GitHub
  - A platform for version control and collaboration, used to host the code repository and manage issues.


- Flask 
  - A micro web framework for Python used to build the API.
- Requests
  - A library for making HTTP requests to interact with the API.
- Tkinter
  - A standard GUI library for Python used to create the user interface of the main app.
- Tkcalendar
    - A calendar widget for Tkinter used to allow users to select dates for their activities.
- JSON
  - A format for storing and exchanging data, used for the API responses and requests.
- Pandas
  - A data manipulation library used for storing the career tracking data in a dataframe format 
  & allowing for O(1) lookups through date indexing

___

## Examples of Use
...

___

## Future Improvements
...

___

## Additional Notes
See the documentation folder for further supporting materials, 
including the SRS document, statement on AI use, accompanying project poster, 
and any other relevant files/diagrams.