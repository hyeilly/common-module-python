from mongoengine import connect, disconnect
from .base import DatabaseClient

class MongoEngineDB(DatabaseClient):
    def __init__(self, db_name: str):
        super().__init__(db_name)

    def __enter__(self):
        try:
            connect(db=self.db_name, host='mongodb://localhost:27017')
            return self
        except Exception as e:
            print(f"Error connecting to MongoDB with MongoEngine: {e}")
            raise

    def __exit__(self, exc_type, exc_value, traceback):
        disconnect()