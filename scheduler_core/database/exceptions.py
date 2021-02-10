from exceptions import BaseSchedulerCoreException


class BaseDatabaseException(BaseSchedulerCoreException):
    """Базовое исключение для работы с базой данных"""
    pass


class UserIsNotFound(BaseDatabaseException):
    """Если пользователь не существует"""
    pass


class ServiceIsNotFound(BaseDatabaseException):
    """Если услуга не существует"""
    pass


class ServiceAlreadyExists(BaseDatabaseException):
    """Если услуга уже существует"""
    pass


class TimetableEntryIsNotFound(BaseDatabaseException):
    """Если запись в расписании не существует"""
    pass
