from enum import Enum


class CommandType(Enum):
    UNKNOWN = -1
    GET_FREE_TIMETABLE_SLOTS = 0
    GET_VISITING_HISTORY = 1
    BOOK_TIMETABLE_SLOT = 3
    GET_WORKERS = 4


class CommandStatus(Enum):
    UNKNOWN = -1
    SUCCESSFUL_EXECUTION = 0
    INTERNAL_ERROR = 1
    SLOT_ALREADY_BUSY = 2
