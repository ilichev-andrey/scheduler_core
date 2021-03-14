import json
import os
from typing import NamedTuple, Dict


class ConnectionConfig(NamedTuple):
    host: str
    port: int


class DatabaseConfig(NamedTuple):
    database: str
    user: str
    password: str
    host: str
    port: int


class Config(NamedTuple):
    log_file: str
    server: ConnectionConfig
    database: DatabaseConfig


def create_config(data: Dict) -> Config:
    """
    :raises
        KeyError если отсутствует параметр в конфиге
        ValueError если указано несоответствующее значение параметра
    """

    server_data = data['server']
    database_data = data['database']
    return Config(
        log_file=data['log_file'],
        server=ConnectionConfig(host=server_data['host'], port=server_data['port']),
        database=DatabaseConfig(
            database=database_data['database'],
            user=database_data['user'],
            password=database_data['password'],
            host=database_data['host'],
            port=database_data['port']
        )
    )


def load_from_env() -> Config:
    """
    :raises
        KeyError если отсутствует параметр в переменных окружения
        ValueError если указано несоответствующее значение параметра
    """

    return Config(
        log_file=str(os.environ['LOG_FILE']),
        server=ConnectionConfig(
            host=str(os.environ['SERVER_HOST']),
            port=int(os.environ['SERVER_PORT'])
        ),
        database=DatabaseConfig(
            database=str(os.environ['DATABASE_NAME']),
            user=str(os.environ['DATABASE_USER']),
            password=str(os.getenv('DATABASE_PASSWORD')),
            host=str(os.getenv('DATABASE_HOST')),
            port=int(os.getenv('DATABASE_PORT'))
        )
    )


def load_from_file(config_file: str) -> Config:
    """
    :raises
        KeyError если отсутствует параметр в конфиге
        ValueError если указано несоответствующее значение параметра
    """

    with open(config_file) as fin:
        config = json.load(fin)

    return create_config(config)


def load(config_file: str) -> Config:
    """
    :raises
        KeyError если отсутствует параметр
        ValueError если указано несоответствующее значение параметра
    """

    if os.path.isfile(config_file):
        return load_from_file(config_file)

    return load_from_env()
