from typing import Dict, Tuple, List, Iterable

from psycopg2 import extras, Error

from scheduler_core import containers
from scheduler_core.database import exceptions
from scheduler_core.database.provider.abstract_provider import AbstractProvider
from wrappers import LoggerWrap


class TimetableProvider(AbstractProvider):
    _TABLE_NAME = 'timetable'

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
            FROM {self._TABLE_NAME}
            WHERE
                worker_id=%s
                AND start_dt>=%s::date
                {where_end_day}
        ''', (worker_id, date_ranges.start_dt.date()))

    def get_by_client_id(self, client_id: int) -> List[containers.TimetableEntry]:
        return self._get(f'''
            SELECT
                timetable.id,
                EXTRACT(epoch FROM timetable.start_dt) AS start_dt,
                EXTRACT(epoch FROM end_dt) AS end_dt,
                services.name AS service_name
            FROM {self._TABLE_NAME}
            LEFT JOIN services ON services.id = timetable.service_id        
            WHERE
                client_id=%s
        ''', (client_id,))

    def sign_up_client(self, entry_ids: Iterable[int], service_ids: Iterable[int], client_id: int) -> None:
        entry_ids = tuple(entry_ids)
        service_ids = tuple(service_ids)

        # Создание запроса и проверка, что слоты в расписании не заняты
        data = {'entry_ids': entry_ids, 'service_ids': service_ids, 'client_id': client_id}
        if not entry_ids or len(entry_ids) != len(service_ids):
            raise exceptions.InvalidInputParameters(
                f'Параметры "entry_ids" и "service_ids" должны быть одинаковой размерности и не пустыми. {data}'
            )

        entry_ids_str = ','.join((str(entry_id) for entry_id in entry_ids))
        select_query = f'''
            SELECT id
            FROM {self._TABLE_NAME}     
            WHERE id IN ({entry_ids_str}) AND client_id IS NULL 
        '''
        cursor = self._db.con.cursor()
        try:
            cursor.execute(select_query)
            entries = cursor.fetchall()
        except Error as e:
            LoggerWrap().get_logger().exception(str(e))
            cursor.close()
            raise exceptions.BaseDatabaseException(f'Не удалось проверить слоты перед записью пользователя. {data}')

        if not entries or len(entries) != len(entry_ids):
            raise exceptions.EntryAlreadyExists('Слоты в расписании уже заняты')

        # Создание запроса и запись пользователя в указанные слоты
        values = []
        for (entry_id, service_id) in zip(entry_ids, service_ids):
            values.append(f'({entry_id}, {client_id}, {service_id})')

        values = ','.join(values)
        update_query = f'''
            UPDATE {self._TABLE_NAME} SET client_id=client_id_new, service_id=service_id_new
            FROM (VALUES {values}) AS tmp(id, client_id_new, service_id_new)
            WHERE timetable.id=tmp.id
        '''
        try:
            cursor.execute(update_query)
        except Error as e:
            LoggerWrap().get_logger().exception(str(e))
            raise exceptions.BaseDatabaseException(f'Не удалось записать пользователя. {data}')
        else:
            self._db.con.commit()
        finally:
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
