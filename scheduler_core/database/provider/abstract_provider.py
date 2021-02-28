from typing import Dict, Iterable

from psycopg2 import Error, errorcodes

from scheduler_core.database import exceptions
from scheduler_core.database.db import DB
from wrappers import LoggerWrap


class AbstractProvider(object):
    _db: DB

    def __init__(self, db: DB):
        self._db = db

    def _add(self, query: str, data: Dict = None) -> None:
        cursor = self._db.con.cursor()
        try:
            cursor.execute(query, data)
            self._db.con.commit()
        except Error as e:
            if e.pgcode == errorcodes.UNIQUE_VIOLATION:
                raise exceptions.EntryAlreadyExists(f'Запись уже существует')

            LoggerWrap().get_logger().exception(f'query="{query}"\ndata={data}')
            raise exceptions.BaseDatabaseException(str(e))
        finally:
            self._db.con.rollback()
            cursor.close()

    def _multi_add(self, table_name, keys: Iterable, values: Iterable) -> None:
        def join_values(_values: Iterable) -> str:
            return '({})'.format(','.join(_values))

        keys = ','.join(keys)
        values = ','.join(join_values(_values) for _values in values)
        self._add(f'''
            INSERT INTO {table_name} ({keys})
            VALUES {values}
        ''')
