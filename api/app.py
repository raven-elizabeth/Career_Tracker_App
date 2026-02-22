# This file defines the API class that sets up the Flask application and its routes.

from flask import Flask, jsonify, request

from database.csv_database_repository import CsvDatabaseRepository
from database.exceptions import FileEmptyError, DuplicateEntryError
from domain.entry import Entry
from domain.fields import FIELDS
from logging_config import get_logger


class API:
    def __init__(self, repository=None, logger=None):
        self.app = Flask(__name__)
        self.app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 # Limit request body size to 16KB
        self._repository = repository if repository is not None else CsvDatabaseRepository()
        self._logger = logger if logger is not None else get_logger(__name__)
        self.setup_routes()

    def setup_routes(self):

        @self.app.route("/api/csv/entries/<date>", methods=["GET"])
        def get_entry_by_date(date):
            self._logger.debug("GET request received for entry with date: %s", date)
            try:
                entry = self._repository.get_entry_by_date(date)
                self._logger.info("Entry retrieved successfully for date: %s", date)
                return jsonify({"message": "Entry retrieved successfully", "data": entry.entry_dict}), 200
            except (FileNotFoundError, FileEmptyError) as e:
                self._logger.error("File unavailable when attempting to retrieve entry for date: %s. Error: %s", date, e)
                return jsonify({"error": "File unavailable"}), 503
            except ValueError:
                self._logger.warning("Entry not found for date: %s", date)
                return jsonify({"error": f"No entry found for date: {date}"}), 404

        @self.app.route("/api/csv/entries", methods=["POST"])
        def post_entry():
            self._logger.debug("POST request received to create a new entry")
            data = request.get_json()
            if not data:
                self._logger.warning("POST request missing JSON body")
                return jsonify({"error": "Invalid JSON body"}), 400

            try:
                # JSON dictionary data is unpacked into keyword arguments for the Entry constructor
                entry = Entry(**data)
            except ValueError as e:
                self._logger.warning("POST request contains invalid data for Entry class: %s", e)
                return jsonify({"error": f"Invalid data for Entry class: {e}"}), 400

            try:
                self._repository.save_entry(entry)
                self._logger.info("Entry saved successfully for date: %s", entry.entry_dict["date"])
                return jsonify({"message": "Entry saved successfully", "data": entry.entry_dict}), 201
            except DuplicateEntryError:
                self._logger.warning("Attempted to save duplicate entry with date: %s", entry.entry_dict["date"])
                return jsonify({"error": f"Entry with date already exists: {entry.entry_dict['date']}"}), 409
            except ValueError:
                self._logger.warning("Failed to save entry for date: %s", entry.entry_dict["date"])
                return jsonify({"error": "Save unsuccessful"}), 400

        @self.app.route("/api/csv/entries/<date>", methods=["PUT"])
        def update_replace_entry(date):
            self._logger.debug("PUT request received to replace entry with date: %s", date)
            data = request.get_json()
            if not data or not all(field in data for field in FIELDS):
                self._logger.warning("PUT request missing JSON body or required fields for Entry class")
                return jsonify({"error": "Invalid JSON body"}), 400

            try:
                updated_entry = Entry(**data)
            except ValueError as e:
                self._logger.warning("PUT request contains invalid data for Entry class: %s", e)
                return jsonify({"error": f"Invalid data for Entry class: {e}"}), 400

            try:
                self._repository.replace_entry(date, updated_entry)
                self._logger.info("Entry replaced successfully for date: %s", date)
                return jsonify({"message": "Entry updated successfully", "data": updated_entry.entry_dict}), 200
            except (FileNotFoundError, FileEmptyError) as e:
                self._logger.error("File unavailable when attempting to retrieve entry for date: %s. Error: %s", date, e)
                return jsonify({"error": "File unavailable"}), 503
            except ValueError as e:
                self._logger.warning("Failed to replace entry for date: %s. %s", date, e)
                return jsonify({"error": f"Update unsuccessful: {e}"}), 404

        @self.app.route("/api/csv/entries/<date>", methods=["PATCH"])
        def partially_update_entry(date):
            self._logger.debug("PATCH request received to partially update entry with date: %s", date)
            update_request = request.get_json()
            if not update_request:
                self._logger.warning("PATCH request missing JSON body")
                return jsonify({"error": "Invalid JSON body"}), 400

            update_items = {k: v for k, v in update_request.items() if k != "date"}
            if all(values == "" for values in update_items.values()):
                self._logger.warning("PATCH request contains no valid fields for update")
                return jsonify({"error": "No valid fields provided for update"}), 400

            # Attempt creating Entry object to pass validation of request data
            try:
                Entry(**update_request)
            except ValueError as e:
                self._logger.warning("PATCH request contains invalid data for Entry class: %s", e)
                return jsonify({"error": f"Invalid data for Entry class: {e}"}), 400

            try:
                updated_entry = self._repository.partially_update_entry(date, update_items)
                self._logger.info("Entry partially updated successfully for date: %s", date)
                return jsonify({"message": "Entry partially updated successfully", "data": updated_entry.entry_dict}), 200
            except (FileNotFoundError, FileEmptyError) as e:
                self._logger.error("File unavailable when attempting to retrieve entry for date: %s. Error: %s", date, e)
                return jsonify({"error": "File unavailable"}), 503
            except ValueError as e:
                self._logger.warning("Failed to partially update entry for date: %s. %s", date, e)
                return jsonify({"error": f"Partial update unsuccessful: {e}"}), 404

        @self.app.route("/api/csv/entries/<date>", methods=["DELETE"])
        def delete_entry(date):
            self._logger.debug("DELETE request received to delete entry with date: %s", date)
            try:
                self._repository.delete_entry(date)
                self._logger.info("Entry deleted successfully for date: %s", date)
                return jsonify({"message": "Entry deleted successfully"}), 200
            except (FileNotFoundError, FileEmptyError) as e:
                self._logger.error("File unavailable when attempting to retrieve entry for date: %s. Error: %s", date, e)
                return jsonify({"error": "File unavailable"}), 503
            except ValueError as e:
                self._logger.warning("Failed to delete entry for date: %s. %s", date, e)
                return jsonify({"error": f"Delete unsuccessful: {e}"}), 404