"""
This file defines the API class that sets up the Flask application and its routes.
The API class uses dependency injection to allow for flexible repository and logger implementations.
The API supports CRUD operations for daily entries, with appropriate error handling and logging.
The API endpoints include:
- GET /api/csv/entries/<date>: Retrieve an entry by date
- POST /api/csv/entries: Create a new entry
- PUT /api/csv/entries/<date>: Replace an existing entry by date
- PATCH /api/csv/entries/<date>: Partially update an existing entry by date
- DELETE /api/csv/entries/<date>: Delete an entry by date

Status codes used:
- 200 OK: Successful retrieval or update of an entry
- 201 Created: Successful creation of a new entry
- 204 No Content: Successful deletion of an entry
- 400 Bad Request: Invalid input data or missing JSON body
- 404 Not Found: Entry not found for the specified date, or no entries exist yet
- 409 Conflict: Attempt to create a duplicate entry with an existing date
- 503 Service Unavailable: File unavailable when attempting to access the repository
Unknown errors will cause a 500 Internal Server Error, which is the default behavior of Flask for unhandled exceptions
Logging will capture details of any exceptions for debugging purposes.
"""

from flask import Flask, jsonify, request

from database.csv_database_repository import CsvDatabaseRepository
from database.exceptions import FileEmptyError, DuplicateEntryError
from domain.dailyentry import DailyEntry
from logging_config import get_logger


class API:
    def __init__(self, repository=None, logger=None):
        self.app = Flask(__name__)
        # Defensive programming
        # Limit maximum content length (16KB) to prevent excessively large requests from being processed
        self.app.config["MAX_CONTENT_LENGTH"] = 16 * 1024

        # Dependency injection
        # Allows for easier testing and flexibility in choosing different repository implementations or loggers
        self._repository = repository if repository is not None else CsvDatabaseRepository()
        self._logger = logger if logger is not None else get_logger(__name__)

        self.setup_routes()

    def setup_routes(self):
        """Register all API route handlers with the Flask application."""

        @self.app.route("/api/csv/entries/<date>", methods=["GET"])
        def get_entry_by_date(date):
            """Retrieve an entry by date.
            Return 200 OK with entry data on success, 404 if no entry found, or 503 if file unavailable."""
            self._logger.debug("GET request received for entry with date: %s", date)
            try:
                entry = self._repository.get_entry_by_date(date)
                if entry:
                    self._logger.info("Entry retrieved successfully for date: %s", date)
                    return jsonify({"message": "Entry retrieved successfully", "data": entry.entry_dict}), 200
                return jsonify({"message": f"No entry found for date: {date}", "entry": entry}), 404
            except (FileNotFoundError, FileEmptyError) as e:
                return self._file_unavailable_response(date, e)

        @self.app.route("/api/csv/entries", methods=["POST"])
        def post_entry():
            """Create a new entry. Return 201 Created on success, 400 Bad Request for invalid input,
            or 409 Conflict if an entry with the same date already exists."""

            self._logger.debug("POST request received to create a new entry")
            data = request.get_json()
            if not data:
                self._logger.warning("POST request missing JSON body")
                return jsonify({"error": "Invalid JSON body"}), 400

            try:
                # JSON dictionary data is unpacked into keyword arguments for the Entry constructor
                entry = DailyEntry(**data)
            except ValueError as e:
                self._logger.warning("POST request contains invalid data for Entry class: %s", e)
                return jsonify({"error": f"Invalid data for Entry class: {e}"}), 400

            try:
                self._repository.save_entry(entry)
                self._logger.info("Entry saved successfully for date: %s", entry.entry_dict["date"])
                return jsonify({"message": "Entry saved successfully", "data": entry.entry_dict}), 201
            except DuplicateEntryError:
                self._logger.warning(
                    "Attempted to save duplicate entry with date: %s",
                    entry.entry_dict["date"]
                )
                return jsonify({"error": f"Entry with date already exists: {entry.entry_dict['date']}"}), 409
            except ValueError:
                self._logger.warning("Failed to save entry for date: %s", entry.entry_dict["date"])
                return jsonify({"error": "Save unsuccessful"}), 400

        @self.app.route("/api/csv/entries/<date>", methods=["PUT"])
        def replace_entry(date):
            """Replace an existing entry by date.
            PUT request replaces entire entry, even if some fields are unchanged.
            Return 200 OK on success, 400 Bad Request for invalid input,
            404 Not Found if entry does not exist for the specified date, or 503 if file unavailable."""

            self._logger.debug("PUT request received to replace entry with date: %s", date)
            data = request.get_json()

            try:
                updated_entry = DailyEntry.from_replace_request(data)
            except ValueError as e:
                self._logger.warning("PUT request contains invalid data for Entry class: %s", e)
                return jsonify({"error": f"Invalid data for Entry class: {e}"}), 400

            try:
                self._repository.replace_entry(date, updated_entry)
                self._logger.info("Entry replaced successfully for date: %s", date)
                return jsonify({"message": "Entry updated successfully", "data": updated_entry.entry_dict}), 200
            except (FileNotFoundError, FileEmptyError) as e:
                return self._file_unavailable_response(date, e)
            except ValueError as e:
                self._logger.warning("Failed to replace entry for date: %s. %s", date, e)
                return jsonify({"error": f"Update unsuccessful: {e}"}), 404

        @self.app.route("/api/csv/entries/<date>", methods=["PATCH"])
        def partially_update_entry(date):
            """Partially update an existing entry by date.
            The benefit to PATCH over PUT is that the request body can be smaller and performance may be improved.
            Return 200 OK on success, 400 Bad Request for invalid input,
            404 Not Found if entry does not exist for the specified date, or 503 if file unavailable."""

            print(f"Received PATCH request for date: {date} with body: {request.get_data()}")
            self._logger.debug("PATCH request received to partially update entry with date: %s", date)
            update_request = request.get_json()
            if not update_request:
                self._logger.warning("PATCH request missing JSON body")
                return jsonify({"error": "Invalid JSON body"}), 400

            # Attempt creating Entry object to pass validation of request data
            try:
                DailyEntry.from_partial_update_request(update_request)
            except ValueError as e:
                self._logger.warning("PATCH request contains invalid data for Entry class: %s", e)
                return jsonify({"error": f"Invalid data for Entry class: {e}"}), 400

            try:
                updated_entry = self._repository.partially_update_entry(update_request)
                self._logger.info("Entry partially updated successfully for date: %s", date)
                return jsonify(
                    {"message": "Entry partially updated successfully", "data": updated_entry.entry_dict}), 200
            except (FileNotFoundError, FileEmptyError) as e:
                return self._file_unavailable_response(date, e)
            except ValueError as e:
                self._logger.warning("Failed to partially update entry for date: %s. %s", date, e)
                return jsonify({"error": f"Partial update unsuccessful: {e}"}), 404

        @self.app.route("/api/csv/entries/<date>", methods=["DELETE"])
        def delete_entry(date):
            """Delete an entry by date.
            Return 204 No Content on success, 404 if entry not found, or 503 if file unavailable."""

            self._logger.debug("DELETE request received to delete entry with date: %s", date)
            try:
                self._repository.delete_entry(date)
                self._logger.info("Entry deleted successfully for date: %s", date)
                return "", 204
            except (FileNotFoundError, FileEmptyError) as e:
                return self._file_unavailable_response(date, e)
            except ValueError as e:
                self._logger.warning("Failed to delete entry for date: %s. %s", date, e)
                return jsonify({"error": f"Delete unsuccessful: {e}"}), 404

    def _file_unavailable_response(self, date, e):
        """Helper method to handle file unavailable errors consistently across endpoints."""
        self._logger.error(
            "File unavailable when attempting to access entry for date: %s. Error: %s",
            date, e
        )
        return jsonify({"error": "File unavailable"}), 503


# Run directly to start the API server; importing this module elsewhere will not start the server
if __name__ == "__main__":
    api = API()
    api.app.run(debug=True)
