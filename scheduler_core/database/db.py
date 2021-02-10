import psycopg2
from psycopg2 import extensions

from configs import DatabaseConfig


class DB(object):
    con: extensions.connection

    def __init__(self, config: DatabaseConfig, password: str):
        self.con = psycopg2.connect(password=password, **config._asdict())

    def __del__(self):
        self.con.close()
