from psycopg2 import extras

from database import containers, exceptions
from database.db import DB
from database.enums import UserType
from wrappers import LoggerWrap


class UserProvider(object):
    def __init__(self, db: DB):
        self._db = db

    def add(self, user: containers.User) -> containers.User:
        LoggerWrap().get_logger().info(f'Добавление пользователя: {user}')
        user = containers.User(user.id, UserType.CLIENT, user.first_name, user.last_name, user.user_name)

        cursor = self._db.con.cursor()
        cursor.execute('''
            INSERT INTO users (id, type, first_name, last_name, user_name)
            VALUES(%(id)s, %(type)s, %(first_name)s, %(last_name)s, %(user_name)s)
        ''', user.asdict())

        self._db.con.commit()
        cursor.close()
        return user

    def get_by_id(self, user_id: int) -> containers.User:
        cursor = self._db.con.cursor(cursor_factory=extras.RealDictCursor)
        cursor.execute('''
            SELECT id, type, first_name, last_name, user_name
            FROM users
            WHERE id=%s
        ''', (user_id,))

        user = cursor.fetchone()
        cursor.close()

        if not user:
            raise exceptions.UserIsNotFound(f'Не найден пользователь с id={user_id}')

        LoggerWrap().get_logger().info(f'Получена запись из таблицы пользователей: {user}')
        return containers.make_user(**user)
