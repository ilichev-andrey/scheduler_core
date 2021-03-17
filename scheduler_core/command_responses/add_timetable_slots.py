from datetime import datetime
from typing import Dict, List

from scheduler_core.command_responses.command_response import CommandResponse
from scheduler_core.enums import CommandType, CommandStatus


class AddTimetableSlotsResponse(CommandResponse):
    dates: List[datetime]

    def __init__(self, command_id: str = None, status: CommandStatus = None, dates: List[datetime] = None):
        super().__init__(command_id=command_id, status=status)
        if dates is None:
            dates = []

        self.dates = dates

    def __str__(self):
        return f'AddTimetableSlotsResponse(id={self.id}, status={self.status}, dates={self.dates})'

    def get_command_type(self) -> CommandType:
        return CommandType.ADD_TIMETABLE_SLOTS

    def _load_data(self, data: Dict) -> bool:
        if not super()._has_keys_in_dict(data, ('dates',)):
            return False

        if not isinstance(data['dates'], List):
            return False

        self.dates = [datetime.fromtimestamp(_date) for _date in data['dates']]
        return True

    def _unload_data(self) -> Dict:
        return {'dates': [_date.timestamp() for _date in self.dates]}
