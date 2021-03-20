from typing import Dict, FrozenSet, List

from scheduler_core.commands.command import Command
from scheduler_core.enums import CommandType


class ReleaseTimetableSlotsCommand(Command):
    timetable_entries: FrozenSet[int]

    def __init__(self, command_id: str = None, timetable_entries: FrozenSet[int] = None):
        super().__init__(command_id=command_id)
        if timetable_entries is None:
            timetable_entries = frozenset()

        self.timetable_entries = timetable_entries

    def __str__(self):
        return f'ReleaseTimetableSlotCommand(id={self.id}, timetable_entries={self.timetable_entries})'

    def get_type(self) -> CommandType:
        return CommandType.RELEASE_TIMETABLE_SLOTS

    def load_from_dict(self, data: Dict) -> bool:
        if not super()._has_keys_in_dict(data, ('timetable_entries',)):
            return False

        if not isinstance(data['timetable_entries'], List):
            return False

        if not super().load_from_dict(data):
            return False

        self.timetable_entries = frozenset(data['timetable_entries'])
        return True

    def to_dict(self) -> Dict:
        data = super().to_dict()
        data.update({
            'timetable_entries': list(self.timetable_entries)
        })
        return data
