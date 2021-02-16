from datetime import datetime
from typing import Dict, List

from scheduler_core.commands.command import Command
from scheduler_core.enums import CommandType


class GetFreeTimetableSlotsCommand(Command):
    day: datetime
    services: frozenset
    worker: int

    def __init__(self, command_id: str = None, day: datetime = None, services: frozenset = None, worker: int = None):
        super().__init__(command_id=command_id)
        if day is None:
            day = datetime.fromtimestamp(0)

        if services is None:
            services = frozenset()

        if worker is None:
            worker = 0

        self.day = day
        self.services = services
        self.worker = worker

    def __str__(self):
        return f'GetFreeTimetableSlotsCommand(id={self.id}, day={self.day}, services={self.services}, '\
               f'worker={self.worker})'

    def get_type(self) -> CommandType:
        return CommandType.GET_FREE_TIMETABLE_SLOTS

    def load_from_dict(self, data: Dict) -> bool:
        if not super()._has_keys_in_dict(data, ('day', 'services', 'worker')):
            return False

        if not isinstance(data['day'], int):
            return False

        if not isinstance(data['services'], List):
            return False

        if not super().load_from_dict(data):
            return False

        self.day = datetime.fromtimestamp(data['day'])
        self.services = frozenset(data['services'])
        self.worker = data['worker']
        return True

    def to_dict(self) -> Dict:
        data = super().to_dict()
        data.update({
            'day': int(self.day.timestamp()),
            'services': list(self.services),
            'worker': self.worker
        })
        return data
