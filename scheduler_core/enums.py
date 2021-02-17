from enum import Enum


class CommandType(Enum):
    UNKNOWN = -1
    GET_FREE_TIMETABLE_SLOTS = 0
    GET_VISITING_HISTORY = 1
    BOOK_TIMETABLE_SLOT = 3
    GET_WORKERS = 4
    GET_SERVICES = 5
    ADD_SERVICES = 6
    ADD_USER = 7
    GET_USER = 8


class CommandStatus(Enum):
    UNKNOWN = -1
    SUCCESSFUL_EXECUTION = 0
    INTERNAL_ERROR = 1
    SLOT_ALREADY_BUSY = 2
    SERVICE_ALREADY_EXISTS = 3
    USER_ALREADY_EXISTS = 4
    USER_IS_NOT_FOUND = 5
    NO_FREE_SLOTS_FOUND = 6


class UserType(Enum):
    UNKNOWN = -1
    WORKER = 0
    CLIENT = 1
