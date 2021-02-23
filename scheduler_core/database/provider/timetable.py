from typing import Dict, Tuple, List

from psycopg2 import extras, Error

from scheduler_core import containers
from scheduler_core.database import exceptions
from scheduler_core.database.provider.abstract_provider import AbstractProvider
from wrappers import LoggerWrap


class TimetableProvider(AbstractProvider):
    def get_by_worker_id(self, worker_id: int, date_ranges: containers.DateRanges) -> List[containers.TimetableEntry]:
        where_end_day = ''
        if date_ranges.end_dt is not None:
            with self._db.con.cursor() as cursor:
                where_end_day = cursor.mogrify('AND start_dt<%(day)s::date+1', {'day': date_ranges.end_dt.date()})
                where_end_day = str(where_end_day, "utf-8")

        return self._get(f'''
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
                worker_id=%s
                AND start_dt>=%s::date
                {where_end_day}
        ''', (worker_id, date_ranges.start_dt.date()))

    def get_by_client_id(self, client_id: int) -> List[containers.TimetableEntry]:
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
        ''', (client_id,))

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
        try:
            cursor.execute(query, values)
            entries = cursor.fetchall()
        except Error as e:
            LoggerWrap().get_logger().exception(str(e))
            raise exceptions.BaseDatabaseException('Ошибка при выполнении запроса')
        finally:
            cursor.close()

        if not entries:
            raise exceptions.TimetableEntryIsNotFound(f'Не найдена ни одна запись в расписании\nquery="{query}"\n'
                                                      f'values={values}')

        LoggerWrap().get_logger().info(f'Получены записи из таблицы расписания: {entries}')
        return [containers.make_timetable_entry(**entry) for entry in entries]
