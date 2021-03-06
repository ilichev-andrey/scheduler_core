from typing import List, Iterable

from psycopg2 import extras, Error

from scheduler_core import containers
from scheduler_core.containers import Service
from scheduler_core.database import exceptions
from scheduler_core.database.provider.abstract_provider import AbstractProvider


class ServiceProvider(AbstractProvider):
    _TABLE_NAME = 'services'

    def get(self) -> List[containers.Service]:
        return self._get('WHERE "enable"=TRUE')

    def get_by_ids(self, ids: Iterable[int]) -> List[containers.Service]:
        ids = ','.join((str(service_id) for service_id in ids))
        return self._get(f'WHERE id IN ({ids}) AND "enable"=TRUE')

    def add(self, service: Service) -> None:
        _service = service
        _service.name.lower()
        self._add(f'''
            INSERT INTO {self._TABLE_NAME} (name, execution_time_minutes)
            VALUES (%(name)s, %(execution_time_minutes)s)
        ''', _service.asdict())

    def multi_add(self, services: List[Service]) -> None:
        service_data = services[0].asdict()
        service_data.pop('id')
        self._multi_add(
            table_name=self._TABLE_NAME,
            keys=service_data.keys(),
            values=((f"'{service.name.lower()}'", service.execution_time_minutes) for service in services)
        )

    def delete(self, ids: Iterable[int]):
        values = ','.join((f'({entry_id})' for entry_id in ids))
        cursor = self._db.con.cursor()
        try:
            cursor.execute(f'''
                UPDATE {self._TABLE_NAME} 
                SET "enable"=FALSE
                FROM (VALUES {values}) AS tmp(id)
                WHERE {self._TABLE_NAME}.id=tmp.id
            ''')
        except Error as e:
            self._db.con.rollback()
            raise exceptions.BaseDatabaseException(str(e))
        else:
            self._db.con.commit()
        finally:
            cursor.close()

    def _get(self, where: str = '') -> List[containers.Service]:
        cursor = self._db.con.cursor(cursor_factory=extras.RealDictCursor)
        try:
            cursor.execute(f'''
                SELECT id, name, execution_time_minutes
                FROM {self._TABLE_NAME}
                {where}
            ''')
            services = cursor.fetchall()
        except Error as e:
            raise exceptions.BaseDatabaseException(str(e))
        finally:
            cursor.close()

        if not services:
            raise exceptions.ServiceIsNotFound(f'Не найдены услуги, where={where}')

        return [containers.make_service(**service) for service in services]
