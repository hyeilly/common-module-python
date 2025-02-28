from abc import ABC, abstractmethod

class DatabaseClient(ABC):
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.client = None
        self.db = None

    @abstractmethod
    def __enter__(self):
        pass

    @abstractmethod
    def __exit__(self, exc_type, exc_value, traceback):
        pass