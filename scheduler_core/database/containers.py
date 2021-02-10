from datetime import datetime
from typing import NamedTuple, Dict

from database.enums import UserType


class User(NamedTuple):
    id: int
    type: UserType
    first_name: str
    last_name: str
    user_name: str

    def asdict(self) -> Dict:
        fields = self._asdict()
        fields['type'] = self.type.value
        return fields


def make_user(**kwargs) -> User:
    return User(type=UserType(kwargs.pop('type')), **kwargs)


class Service(NamedTuple):
    id: int
    name: str
    execution_time_minutes: int

    def asdict(self) -> Dict:
        return self._asdict()


def make_service(**kwargs) -> Service:
    return Service(**kwargs)


class TimetableEntry(NamedTuple):
    id: int
    worker_id: int = None
    client_id: int = None
    service_id: int = None
    service_name: str = None
    create_dt: datetime = None
    start_dt: datetime = None
    end_dt: datetime = None


def make_timetable_entry(**kwargs):
    create_dt = kwargs.pop('create_dt', None)
    if create_dt is not None:
        create_dt = datetime.fromtimestamp(create_dt)

    start_dt = kwargs.pop('start_dt', None)
    if start_dt is not None:
        start_dt = datetime.fromtimestamp(start_dt)

    end_dt = kwargs.pop('end_dt', None)
    if end_dt is not None:
        end_dt = datetime.fromtimestamp(end_dt)

    return TimetableEntry(create_dt=create_dt, start_dt=start_dt, end_dt=end_dt, **kwargs)
