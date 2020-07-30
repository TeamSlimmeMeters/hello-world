from abc import ABC, abstractmethod
from sanne_test_python.move import common

class BaseConnector(ABC):
    '''
    The Abstract class for all connectors
    '''

    host: str = None
    port: str = None
    connection_string: str = None
    connection = None
    cursor = None

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def connect(self, database_settings: common.DatabaseSettings):
        pass

    @abstractmethod
    def cursor_execute(self, query: str):
        pass