from pymongo import MongoClient
from .base import DatabaseClient

class MongoDB(DatabaseClient):
    def __init__(self, db_name: str):
        super().__init__(db_name)

    def __enter__(self):
        try:
            self.client = MongoClient('mongodb://localhost:27017')
            self.db = self.client[self.db_name]
            return self.db
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")
            raise

    def __exit__(self, exc_type, exc_value, traceback):
        if self.client:
            self.client.close()