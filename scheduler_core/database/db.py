import psycopg2
from psycopg2 import extensions

from scheduler_core.configs import DatabaseConfig


class DB(object):
    con: extensions.connection

    def __init__(self, config: DatabaseConfig):
        self.con = psycopg2.connect(password=config.password, **config._asdict())

    def __del__(self):
        self.con.close()
