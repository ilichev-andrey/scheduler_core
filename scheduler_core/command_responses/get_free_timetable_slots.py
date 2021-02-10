from typing import Dict, List

from command_responses.command_response import CommandResponse
from enums import CommandStatus


class GetFreeTimetableSlotsResponse(CommandResponse):
    timetable_ids: List[int]

    def __init__(self, command_id: str = None, status: CommandStatus = None, timetable_ids: List[int] = None):
        super().__init__(command_id=command_id, status=status)
        if timetable_ids is None:
            timetable_ids = []

        self.timetable_ids = timetable_ids

    def load_from_dict(self, data: Dict) -> bool:
        if not super()._has_keys_in_dict(data, ('timetable',)):
            return False

        if not isinstance(data['timetable'], List):
            return False

        if not super().load_from_dict(data):
            return False

        self.timetable_ids = data['timetable']
        return True

    def to_dict(self) -> Dict:
        data = super().to_dict()
        data.update({
            'timetable': self.timetable_ids
        })
        return data
