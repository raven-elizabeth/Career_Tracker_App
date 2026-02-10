from flask import Flask, jsonify, request

class API:
    def __init__(self):
        self.app = Flask(__name__)
        self.setup_routes()

    def setup_routes(self):

        @self.app.route('/api/entries', methods=['GET'])
        def get_data():
            pass
            # Read data from csv...
            # Return data as JSON

        @self.app.route('/api/entries', methods=['POST'])
        def post_data():
            entry = request.get_json()

            if not entry:
                return jsonify({'error': 'No data provided'}), 400

            # Save entry to csv...

            return jsonify({'message': 'Entry saved successfully', 'entry': entry}), 201

    def run(self, debug=True):
        self.app.run(debug=debug)