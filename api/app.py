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

        @self.app.route('/api/csv/entries', methods=['GET'])
        def get_data():
            pass
            # Read data from csv...
            # Return data as JSON

        @self.app.route('/api/csv/entries', methods=['POST'])
        def post_data():
            data = request.get_json()
            if not data:
                return jsonify({'error': 'No data provided'}), 400

            entry = Entry(**data) # JSON dictionary data is unpacked into keyword arguments for the Entry constructor
            self.repository.save_entry(entry)
            return jsonify({'message': 'Entry saved successfully', 'entry': entry.entry_dict}), 201

    def run(self, debug=True):
        self.app.run(debug=debug)