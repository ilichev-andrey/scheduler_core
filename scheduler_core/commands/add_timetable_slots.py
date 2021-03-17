from datetime import time
from typing import Dict, List

from scheduler_core.commands.command import Command
from scheduler_core.containers import DateRanges, make_date_ranges
from scheduler_core.enums import CommandType


class AddTimetableSlotsCommand(Command):
    date_ranges: DateRanges
    times: List[time]
    worker: int

    def __init__(self, command_id: str = None, date_ranges: DateRanges = None, times: List[time] = None,
                 worker: int = None):
        super().__init__(command_id=command_id)
        if date_ranges is None:
            date_ranges = DateRanges()

        if times is None:
            times = []

        if worker is None:
            worker = 0

        self.date_ranges = date_ranges
        self.times = times
        self.worker = worker

    def __str__(self):
        return f'AddTimetableSlotsCommand(id={self.id}, date_ranges={self.date_ranges}, times={self.times}, '\
               f'worker={self.worker})'

    def get_type(self) -> CommandType:
        return CommandType.ADD_TIMETABLE_SLOTS

    def load_from_dict(self, data: Dict) -> bool:
        if not super()._has_keys_in_dict(data, ('date_ranges', 'times', 'worker')):
            return False

        if not isinstance(data['date_ranges'], Dict):
            return False

        if not isinstance(data['times'], List):
            return False

        if not super().load_from_dict(data):
            return False

        self.date_ranges = make_date_ranges(**data['date_ranges'])
        self.times = self._times_from_strings(data['times'])
        self.worker = data['worker']
        return True

    def to_dict(self) -> Dict:
        data = super().to_dict()
        data.update({
            'date_ranges': self.date_ranges.asdict(),
            'times': self._times_to_strings(),
            'worker': self.worker
        })
        return data

    @staticmethod
    def _times_from_strings(times: List[str]) -> List[time]:
        return list((time.fromisoformat(_time) for _time in times))

    def _times_to_strings(self) -> List[str]:
        return list((_time.strftime('%H:%M') for _time in self.times))
