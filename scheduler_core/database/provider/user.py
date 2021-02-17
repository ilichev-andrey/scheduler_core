from typing import List

from psycopg2 import extras

from scheduler_core import containers
from scheduler_core.database import exceptions
from scheduler_core.database.provider.abstract_provider import AbstractProvider
from scheduler_core.enums import UserType
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
        return self._get(f'WHERE id={int(user_id)}')

    def get_buy_messenger_id(self, telegram_id: int, viber_id: int) -> containers.User:
        if isinstance(telegram_id, int):
            where = f'telegram_id={telegram_id}'
        elif isinstance(viber_id, int):
            where = f'viber_id={viber_id}'
        else:
            raise exceptions.InvalidInputParameters(
                f'Получены невалидные данные, telegram_id={telegram_id}, viber_id={viber_id}'
            )

        return self._get(f'WHERE {where}')

    def _get(self, where: str = '') -> containers.User:
        cursor = self._db.con.cursor(cursor_factory=extras.RealDictCursor)
        cursor.execute(f'''
            SELECT id, type, first_name, last_name, phone_number, telegram_id, telegram_name, viber_id, viber_name
            FROM {self._TABLE_NAME}
            {where}
        ''')

        user = cursor.fetchone()
        cursor.close()

        if not user:
            raise exceptions.UserIsNotFound(f'Пользователь не найден, where="{where}"')

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
            raise exceptions.UserIsNotFound(f'Не найдены работники')

        return [containers.make_user(**user) for user in users]
