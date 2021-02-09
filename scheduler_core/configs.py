from typing import NamedTuple, Dict


class ServerConfig(NamedTuple):
    host: str
    port: int


class Config(NamedTuple):
    log_file: str
    server: ServerConfig


def load_config(data: Dict) -> Config:
    """
    :raises
        KeyError если отсутствует параметр в конфиге
    """

    server_data = data['server']
    return Config(
        log_file=data['log_file'],
        server=ServerConfig(host=server_data['host'], port=server_data['port'])
    )
