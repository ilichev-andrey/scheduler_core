from typing import Dict, FrozenSet, List

from scheduler_core.commands.command import Command
from scheduler_core.containers import DateRanges, make_date_ranges
from scheduler_core.enums import CommandType


class GetFreeTimetableSlotsCommand(Command):
    date_ranges: DateRanges
    services: FrozenSet[int]
    worker: int

    def __init__(self, command_id: str = None, date_ranges: DateRanges = None, services: FrozenSet[int] = None,
                 worker: int = None):
        super().__init__(command_id=command_id)
        if date_ranges is None:
            date_ranges = DateRanges()

        if services is None:
            services = frozenset()

        if worker is None:
            worker = 0

        self.date_ranges = date_ranges
        self.services = services
        self.worker = worker

    def __str__(self):
        return f'GetFreeTimetableSlotsCommand(id={self.id}, date_ranges={self.date_ranges}, services={self.services}, '\
               f'worker={self.worker})'

    def get_type(self) -> CommandType:
        return CommandType.GET_FREE_TIMETABLE_SLOTS

    def load_from_dict(self, data: Dict) -> bool:
        if not super()._has_keys_in_dict(data, ('date_ranges', 'services', 'worker')):
            return False

        if not isinstance(data['date_ranges'], Dict):
            return False

        if not isinstance(data['services'], List):
            return False

        if not super().load_from_dict(data):
            return False

        self.date_ranges = make_date_ranges(**data['date_ranges'])
        self.services = frozenset(data['services'])
        self.worker = data['worker']
        return True

    def to_dict(self) -> Dict:
        data = super().to_dict()
        data.update({
            'date_ranges': self.date_ranges.asdict(),
            'services': list(self.services),
            'worker': self.worker
        })
        return data
