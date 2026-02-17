import tempfile
from os import path
from database.csv_database_repository import CsvDatabaseRepository

test_dir = tempfile.TemporaryDirectory()
test_file_path = path.join(test_dir.name, "test_entries.csv")
test_repository = CsvDatabaseRepository(file_path=test_file_path)