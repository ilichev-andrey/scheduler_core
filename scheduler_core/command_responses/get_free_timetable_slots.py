from typing import Dict, List

from scheduler_core.command_responses.command_response import CommandResponse
from scheduler_core.enums import CommandStatus, CommandType


class GetFreeTimetableSlotsResponse(CommandResponse):
    timetable_ids: List[int]

    def __init__(self, command_id: str = None, status: CommandStatus = None, timetable_ids: List[int] = None):
        super().__init__(command_id=command_id, status=status)
        if timetable_ids is None:
            timetable_ids = []

        self.timetable_ids = timetable_ids

    def get_command_type(self) -> CommandType:
        return CommandType.GET_FREE_TIMETABLE_SLOTS

    def _load_data(self, data: Dict) -> bool:
        if not super()._has_keys_in_dict(data, ('timetable',)):
            return False

        if not isinstance(data['timetable'], List):
            return False

        self.timetable_ids = data['timetable']
        return True

    def _unload_data(self) -> Dict:
        return {'timetable': self.timetable_ids}
