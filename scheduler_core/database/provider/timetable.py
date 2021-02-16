from datetime import date
from typing import Dict, Tuple, List

from psycopg2 import extras

from scheduler_core.database import exceptions, containers
from scheduler_core.database.provider.abstract_provider import AbstractProvider
from wrappers import LoggerWrap


class TimetableProvider(AbstractProvider):
    def get(self) -> List[containers.TimetableEntry]:
        return self._get('''
             SELECT
                 id,
                 worker_id,
                 client_id,
                 service_id,
                 EXTRACT(epoch FROM create_dt) AS create_dt,
                 EXTRACT(epoch FROM start_dt) AS start_dt,
                 EXTRACT(epoch FROM end_dt) AS end_dt
             FROM timetable
             WHERE client_id ISNULL
        ''')

    def get_for_day(self, day: date, worker: int) -> List[containers.TimetableEntry]:
        return self._get('''
            SELECT
                id,
                worker_id,
                client_id,
                service_id,
                EXTRACT(epoch FROM create_dt) AS create_dt,
                EXTRACT(epoch FROM start_dt) AS start_dt,
                EXTRACT(epoch FROM end_dt) AS end_dt
            FROM timetable
            WHERE
                worker_id=%(worker_id)s
                AND start_dt>=%(day)s::date
                AND start_dt<%(day)s::date+1
        ''', {'worker_id': worker, 'day': day})

    def get_by_user_id(self, user_id: int) -> List[containers.TimetableEntry]:
        return self._get('''
            SELECT
                timetable.id,
                EXTRACT(epoch FROM timetable.start_dt) AS start_dt,
                EXTRACT(epoch FROM end_dt) AS end_dt,
                services.name AS service_name
            FROM timetable
            LEFT JOIN services ON services.id = timetable.service_id        
            WHERE
                client_id=%s
        ''', (user_id,))

    def update_entry(self, timetable_id: int, service_id: int, user_id: int):
        cursor = self._db.con.cursor()
        cursor.execute('''
            UPDATE timetable
            SET client_id=%s, service_id=%s
            WHERE id=%s
        ''', (user_id, service_id, timetable_id))

        self._db.con.commit()
        cursor.close()

    def _get(self, query: str, values: Dict or Tuple = None):
        cursor: extras.RealDictCursor = self._db.con.cursor(cursor_factory=extras.RealDictCursor)
        cursor.execute(query, values)

        entries = cursor.fetchall()
        cursor.close()

        LoggerWrap().get_logger().info(f'Получены записи из таблицы расписания: {entries}')
        if not entries:
            raise exceptions.TimetableEntryIsNotFound(f'Не найдена ни одна запись в расписании')

        return [containers.make_timetable_entry(**entry) for entry in entries]
