from typing import List

from psycopg2 import extras

from database import containers, exceptions
from database.enums import UserType
from database.provider.abstract_provider import AbstractProvider
from wrappers import LoggerWrap


class UserProvider(AbstractProvider):
    _TABLE_NAME = 'users'

    def add(self, user: containers.User) -> None:
        LoggerWrap().get_logger().info(f'Добавление пользователя: {user}')

        self._add(f'''
            INSERT INTO {self._TABLE_NAME}
            (type, first_name, last_name, phone_number, telegram_id, telegram_name, viber_id, viber_name)
            VALUES (
                %(type)s,
                %(first_name)s,
                %(last_name)s, 
                %(phone_number)s,
                %(telegram_id)s,
                %(telegram_name)s,
                %(viber_id)s,
                %(viber_name)s
            )
        ''', user.asdict())

    def get_by_id(self, user_id: int) -> containers.User:
        cursor = self._db.con.cursor(cursor_factory=extras.RealDictCursor)
        cursor.execute(f'''
            SELECT id, type, first_name, last_name, phone_number, telegram_id, telegram_name, viber_id, viber_name
            FROM {self._TABLE_NAME}
            WHERE id=%s
        ''', (user_id,))

        user = cursor.fetchone()
        cursor.close()

        if not user:
            raise exceptions.UserIsNotFound(f'Не найден пользователь с id={user_id}')

        LoggerWrap().get_logger().info(f'Получена запись из таблицы пользователей: {user}')
        return containers.make_user(**user)

    def get_workers(self) -> List[containers.User]:
        cursor = self._db.con.cursor(cursor_factory=extras.RealDictCursor)
        cursor.execute(f'''
            SELECT id, type, first_name, last_name, phone_number, telegram_id, telegram_name, viber_id, viber_name
            FROM {self._TABLE_NAME}
            WHERE type=%s
        ''', (UserType.WORKER.value,))

        users = cursor.fetchall()
        cursor.close()

        if not users:
            raise exceptions.UserIsNotFound(f'Не найдены пользователи')

        return [containers.make_user(**user) for user in users]
