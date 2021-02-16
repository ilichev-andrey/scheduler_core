from scheduler_core.exceptions import BaseSchedulerCoreException


class BaseDatabaseException(BaseSchedulerCoreException):
    """Базовое исключение для работы с базой данных"""
    pass


class UserIsNotFound(BaseDatabaseException):
    """Если пользователь не существует"""
    pass


class ServiceIsNotFound(BaseDatabaseException):
    """Если услуга не существует"""
    pass


class EntryAlreadyExists(BaseDatabaseException):
    """Если запись уже существует в таблице"""
    pass


class TimetableEntryIsNotFound(BaseDatabaseException):
    """Если запись в расписании не существует"""
    pass


class InvalidInputParameters(BaseDatabaseException):
    """Если получены невалидные данные для БД"""
    pass
