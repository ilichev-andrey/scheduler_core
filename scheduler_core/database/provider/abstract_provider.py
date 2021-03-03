from typing import Dict, Iterable

from psycopg2 import Error, errorcodes

from scheduler_core.database import exceptions
from scheduler_core.database.db import DB
from wrappers import LoggerWrap


def filter_not_none_values(data: Dict) -> Dict:
    return {key: val for key, val in data.items() if val is not None}


def create_set_values_str(data: Dict) -> str:
    if not data:
        return ''

    set_str = ','.join((f'{key}=%({key})s' for key in data))
    return f'SET {set_str}'


class AbstractProvider(object):
    _db: DB

    def __init__(self, db: DB):
        self._db = db

    def _add(self, query: str, data: Dict = None) -> None:
        cursor = self._db.con.cursor()
        try:
            cursor.execute(query, data)
        except Error as e:
            self._db.con.rollback()
            if e.pgcode == errorcodes.UNIQUE_VIOLATION:
                raise exceptions.EntryAlreadyExists(f'Запись уже существует')

            LoggerWrap().get_logger().exception(f'query="{query}"\ndata={data}')
            raise exceptions.BaseDatabaseException(str(e))
        else:
            self._db.con.commit()
        finally:
            cursor.close()

    def _multi_add(self, table_name: str, keys: Iterable, values: Iterable) -> None:
        def join_values(_values: Iterable) -> str:
            return '({})'.format(','.join(_values))

        keys = ','.join(keys)
        values = ','.join(join_values(_values) for _values in values)
        self._add(f'''
            INSERT INTO {table_name} ({keys})
            VALUES {values}
        ''')

    def _update_data(self, table_name: str, entry_id: int, data: Dict) -> None:
        data = filter_not_none_values(data)
        data['id'] = entry_id
        cursor = self._db.con.cursor()
        try:
            cursor.execute(f'''
                UPDATE {table_name} 
                {create_set_values_str(data)}
                WHERE {table_name}.id=%(id)s
            ''', data)
        except Error as e:
            self._db.con.rollback()
            LoggerWrap().get_logger().exception(str(e))
            raise exceptions.BaseDatabaseException(f'Не удалось обновить данные. {data}')
        else:
            self._db.con.commit()
        finally:
            cursor.close()
