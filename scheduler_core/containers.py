from datetime import datetime
from typing import NamedTuple, Dict

from scheduler_core.enums import UserType


class DateRanges(NamedTuple):
    start_dt: datetime = None
    end_dt: datetime = None

    def asdict(self) -> Dict:
        data = self._asdict()
        if self.start_dt is not None:
            data['start_dt'] = int(self.start_dt.timestamp())
        if self.end_dt is not None:
            data['end_dt'] = int(self.end_dt.timestamp())

        return data


def make_date_ranges(**kwargs) -> DateRanges:
    start_dt = kwargs.pop('start_dt', None)
    if start_dt is not None:
        start_dt = datetime.fromtimestamp(start_dt)

    end_dt = kwargs.pop('end_dt', None)
    if end_dt is not None:
        end_dt = datetime.fromtimestamp(end_dt)

    return DateRanges(start_dt=start_dt, end_dt=end_dt)


class User(NamedTuple):
    id: int = None
    type: UserType = None
    first_name: str = None
    last_name: str = None
    phone_number: str = None
    telegram_id: int = None
    telegram_name: str = None
    viber_id: int = None
    viber_name: str = None

    def asdict(self) -> Dict:
        fields = self._asdict()

        if isinstance(fields['type'], UserType):
            fields['type'] = self.type.value
        else:
            fields['type'] = UserType.UNKNOWN.value

        return fields


def make_user(**kwargs) -> User:
    user_type = kwargs.pop('type', None)
    if user_type is None:
        user_type = UserType.UNKNOWN

    return User(type=UserType(user_type), **kwargs)


class Service(NamedTuple):
    name: str
    execution_time_minutes: int
    id: int = None

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

    def asdict(self) -> Dict:
        data = self._asdict()
        if self.create_dt is not None:
            data['create_dt'] = int(self.create_dt.timestamp())
        if self.start_dt is not None:
            data['start_dt'] = int(self.start_dt.timestamp())
        if self.end_dt is not None:
            data['end_dt'] = int(self.end_dt.timestamp())

        return data


def make_timetable_entry(**kwargs) -> TimetableEntry:
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
