from typing import List, Iterable

from psycopg2 import Error, errorcodes
from psycopg2 import extras

from database import containers, exceptions
from database.db import DB


class ServiceProvider(object):
    def __init__(self, db: DB):
        self._db = db

    def get(self) -> List[containers.Service]:
        return self._get('WHERE "enable" = TRUE')

    def get_by_ids(self, ids: Iterable[int]) -> List[containers.Service]:
        ids = ','.join((str(service_id) for service_id in ids))
        return self._get(f'WHERE id IN ({ids}) AND "enable" = TRUE')

    def add(self, name: str):
        cursor = self._db.con.cursor()
        try:
            cursor.execute('''
                INSERT INTO services (name)
                VALUES (%s)
            ''', (name,))
            self._db.con.commit()
        except Error as e:
            if e.pgcode == errorcodes.UNIQUE_VIOLATION:
                raise exceptions.ServiceAlreadyExists(f'{name} уже существует')
            raise exceptions.BaseDatabaseException(str(e))
        finally:
            cursor.close()

    def _get(self, where: str = '') -> List[containers.Service]:
        cursor = self._db.con.cursor(cursor_factory=extras.RealDictCursor)
        cursor.execute(f'''
            SELECT id, name, execution_time_minutes
            FROM services
            {where}
        ''')

        services = cursor.fetchall()
        cursor.close()

        if not services:
            raise exceptions.ServiceIsNotFound(f'Не найдена ни одна услуга')

        return [containers.make_service(**service) for service in services]
