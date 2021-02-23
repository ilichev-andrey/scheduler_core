from typing import Dict, FrozenSet, List

from scheduler_core.commands.command import Command
from scheduler_core.enums import CommandType


class TakeTimetableSlotsCommand(Command):
    timetable_entries: FrozenSet[int]
    services: FrozenSet[int]
    client: int

    def __init__(self, command_id: str = None, timetable_entries: FrozenSet[int] = None,
                 services: FrozenSet[int] = None, client: int = None):
        super().__init__(command_id=command_id)
        if timetable_entries is None:
            timetable_entries = frozenset()

        if services is None:
            services = frozenset()

        if client is None:
            client = 0

        self.timetable_entries = timetable_entries
        self.services = services
        self.client = client

    def __str__(self):
        return f'TakeTimetableSlotsCommand(id={self.id}, timetable_entries={self.timetable_entries}, ' \
               f'services={self.services}, client={self.client})'

    def get_type(self) -> CommandType:
        return CommandType.TAKE_TIMETABLE_SLOTS

    def load_from_dict(self, data: Dict) -> bool:
        if not super()._has_keys_in_dict(data, ('timetable_entries', 'services', 'client')):
            return False

        if not isinstance(data['timetable_entries'], List):
            return False

        if not isinstance(data['services'], List):
            return False

        if not super().load_from_dict(data):
            return False

        self.timetable_entries = frozenset(data['timetable_entries'])
        self.services = frozenset(data['services'])
        self.client = data['client']
        return True

    def to_dict(self) -> Dict:
        data = super().to_dict()
        data.update({
            'timetable_entries': list(self.timetable_entries),
            'services': list(self.services),
            'client': self.client
        })
        return data
