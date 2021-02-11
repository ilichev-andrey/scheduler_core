from typing import List, Iterable

from psycopg2 import extras

from database import containers, exceptions
from database.containers import Service
from database.provider.abstract_provider import AbstractProvider


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
        ''', service.asdict())

    def multi_add(self, services: List[Service]) -> None:
        service_data = services[0].asdict()
        service_data.pop('id')
        keys = ','.join(service_data.keys())
        values = ','.join(f"('{service.name.lower()}', {service.execution_time_minutes})" for service in services)
        self._add(f'''
            INSERT INTO {self._TABLE_NAME} ({keys})
            VALUES {values}
        ''')

    def _get(self, where: str = '') -> List[containers.Service]:
        cursor = self._db.con.cursor(cursor_factory=extras.RealDictCursor)
        cursor.execute(f'''
            SELECT id, name, execution_time_minutes
            FROM {self._TABLE_NAME}
            {where}
        ''')

        services = cursor.fetchall()
        cursor.close()

        if not services:
            raise exceptions.ServiceIsNotFound(f'Не найдены услуги')

        return [containers.make_service(**service) for service in services]
