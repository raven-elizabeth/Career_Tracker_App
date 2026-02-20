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

        @self.app.route('/api/csv/entries/<date>', methods=['GET'])
        def get_data_by_date(date):
            try:
                entry = self.repository.get_entry_by_date(date)
                return jsonify({"data": entry.entry_dict}), 200
            except ValueError:
                return jsonify({"error": f"No entry found for date: {date}"}), 404

        @self.app.route('/api/csv/entries', methods=['POST'])
        def post_data():
            try:
                data = request.get_json()
                # JSON dictionary data is unpacked into keyword arguments for the Entry constructor
                entry = Entry(**data)
                self.repository.save_entry(entry)
                return jsonify({'message': 'Entry saved successfully', 'entry': entry.entry_dict}), 201
            except ValueError:
                return jsonify({'error': 'No data provided'}), 400



    def run(self, debug=True):
        self.app.run(debug=debug)