# This file defines the API class that sets up the Flask application and its routes.

from flask import Flask, jsonify, request
from database.csv_database_repository import CsvDatabaseRepository
from domain.entry import Entry
from domain.fields import fields


class API:
    def __init__(self, repository=None):
        self.app = Flask(__name__)
        self.repository = repository if repository is not None else CsvDatabaseRepository()
        self.setup_routes()

    def setup_routes(self):

        @self.app.route("/api/csv/entries/<date>", methods=["GET"])
        def get_entry_by_date(date):
            try:
                entry = self.repository.get_entry_by_date(date)
                return jsonify({"message": "Entry retrieved successfully", "data": entry.entry_dict}), 200
            except ValueError:
                return jsonify({"error": f"No entry found for date: {date}"}), 404

        @self.app.route("/api/csv/entries", methods=["POST"])
        def post_entry():
            data = request.get_json()
            if not data:
                return jsonify({"error": "Invalid JSON body"}), 400

            try:
                # JSON dictionary data is unpacked into keyword arguments for the Entry constructor
                entry = Entry(**data)
            except ValueError as e:
                return jsonify({"error": f"Invalid data for Entry class: {str(e)}"}), 400

            try:
                self.repository.save_entry(entry)
                return jsonify({"message": "Entry saved successfully", "data": entry.entry_dict}), 201
            except ValueError:
                return jsonify({"error": "Save unsuccessful"}), 400

        @self.app.route("/api/csv/entries/<date>", methods=["PUT"])
        def update_replace_entry(date):
            data = request.get_json()
            if not data or not all(field in data for field in fields):
                return jsonify({"error": "Invalid JSON body"}), 400

            try:
                updated_entry = Entry(**data)
            except ValueError as e:
                return jsonify({"error": f"Invalid data for Entry class: {str(e)}"}), 400

            try:
                self.repository.replace_entry(date, updated_entry)
                return jsonify({"message": "Entry updated successfully", "data": updated_entry.entry_dict}), 200
            except ValueError as e:
                return jsonify({"error": f"Update unsuccessful: {str(e)}"}), 404

        @self.app.route("/api/csv/entries/<date>", methods=["PATCH"])
        def partially_update_entry(date):
            update_request = request.get_json()
            if not update_request:
                return jsonify({"error": "Invalid JSON body"}), 400

            update_items = {k: v for k, v in update_request.items() if k != "date"}
            if all(values == "" for values in update_items.values()):
                return jsonify({"error": "No valid fields provided for update"}), 400

            try:
                update_fields_as_entry = Entry(**update_request)
            except ValueError as e:
                return jsonify({"error": f"Invalid data for Entry class: {str(e)}"}), 400

            try:
                updated_entry = self.repository.partially_update_entry(date, update_fields_as_entry.entry_dict)
                return jsonify({"message": "Entry partially updated successfully", "data": updated_entry.entry_dict}), 200
            except ValueError as e:
                return jsonify({"error": f"Partial update unsuccessful: {str(e)}"}), 404

        @self.app.route("/api/csv/entries/<date>", methods=["DELETE"])
        def delete_entry(date):
            try:
                self.repository.delete_entry(date)
                return jsonify({"message": "Entry deleted successfully"}), 200
            except ValueError:
                return jsonify({"error": "Delete unsuccessful"}), 404


    def run(self, debug=True):
        self.app.run(debug=debug)