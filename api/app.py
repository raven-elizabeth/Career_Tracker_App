# This file defines the API class that sets up the Flask application and its routes.

from flask import Flask, jsonify, request
from database.csv_database_repository import CsvDatabaseRepository
from domain.entry import Entry


class API:
    def __init__(self, repository=CsvDatabaseRepository()):
        self.app = Flask(__name__)
        self.setup_routes()
        self.repository = repository

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
            try:
                data = request.get_json()
                # JSON dictionary data is unpacked into keyword arguments for the Entry constructor
                entry = Entry(**data)
                self.repository.save_entry(entry)
                return jsonify({"message": "Entry saved successfully", "data": entry.entry_dict}), 201
            except ValueError:
                return jsonify({"error": "Save unsuccessful"}), 400

        @self.app.route("/api/csv/entries/<date>", methods=["PUT"])
        def update_entry(date):
            try:
                data = request.get_json()
                updated_entry = Entry(**data)
                self.repository.update_entry(date, updated_entry)
                return jsonify({"message": "Entry updated successfully", "data": updated_entry.entry_dict}), 200
            except ValueError:
                return jsonify({"error": "Update unsuccessful"}), 404

        @self.app.route("/api/csv/entries/<date>", methods=["DELETE"])
        def delete_entry(date):
            try:
                self.repository.delete_entry(date)
                return jsonify({"message": "Entry deleted successfully"}), 200
            except ValueError:
                return jsonify({"error": "Delete unsuccessful"}), 404



    def run(self, debug=True):
        self.app.run(debug=debug)