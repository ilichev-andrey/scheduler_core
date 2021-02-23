from typing import Dict, List

from scheduler_core.command_responses.command_response import CommandResponse
from scheduler_core.containers import TimetableEntry, make_timetable_entry
from scheduler_core.enums import CommandStatus, CommandType


class GetFreeTimetableSlotsResponse(CommandResponse):
    timetable_entries: List[TimetableEntry]

    def __init__(self, command_id: str = None, status: CommandStatus = None,
                 timetable_entries: List[TimetableEntry] = None):
        super().__init__(command_id=command_id, status=status)
        if timetable_entries is None:
            timetable_entries = []

        self.timetable_entries = timetable_entries

    def __str__(self):
        return f'GetFreeTimetableSlotsResponse(id={self.id}, status={self.status}, ' \
               f'timetable_entries={self.timetable_entries})'

    def get_command_type(self) -> CommandType:
        return CommandType.GET_FREE_TIMETABLE_SLOTS

    def _load_data(self, data: Dict) -> bool:
        if not super()._has_keys_in_dict(data, ('timetable',)):
            return False

        if not isinstance(data['timetable'], List):
            return False

        self.timetable_entries = [make_timetable_entry(**entry_data) for entry_data in data['timetable']]
        return True

    def _unload_data(self) -> Dict:
        return {'timetable': [timetable_entry.asdict() for timetable_entry in self.timetable_entries]}
