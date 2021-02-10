from typing import NamedTuple, Dict


class ServerConfig(NamedTuple):
    host: str
    port: int


class DatabaseConfig(NamedTuple):
    database: str
    user: str
    host: str
    port: int


class Config(NamedTuple):
    log_file: str
    server: ServerConfig
    database: DatabaseConfig


def load_config(data: Dict) -> Config:
    """
    :raises
        KeyError если отсутствует параметр в конфиге
    """

    server_data = data['server']
    database_data = data['database']
    return Config(
        log_file=data['log_file'],
        server=ServerConfig(host=server_data['host'], port=server_data['port']),
        database=DatabaseConfig(
            database=database_data['database'],
            user=database_data['user'],
            host=database_data['host'],
            port=database_data['port']
        )
    )
