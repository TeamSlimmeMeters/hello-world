from typing import Dict
import inspect


def get_caller():
    return inspect.stack()[-1].filename


class DatabaseSettings:
    username: str
    password: str
    database: str
    instance: str
    connection_type: str = "direct"
    driver_path: str


class CommonSettings:
    environment: str
    databaseSettings: Dict[str, DatabaseSettings]

