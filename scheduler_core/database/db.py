import psycopg2
from psycopg2 import extensions

from scheduler_core.configs import DatabaseConfig


class DB(object):
    con: extensions.connection = None

    def __init__(self, config: DatabaseConfig):
        self.con = psycopg2.connect(**config._asdict())

    def __del__(self):
        if self.con is not None:
            self.con.close()
