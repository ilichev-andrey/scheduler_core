from scheduler_core.command_responses.get_timetable import GetTimetableResponse
from scheduler_core.enums import CommandType


class GetFreeTimetableSlotsResponse(GetTimetableResponse):
    def __str__(self):
        return f'GetFreeTimetableSlotsResponse(id={self.id}, status={self.status}, ' \
               f'timetable_entries={self.timetable_entries})'

    def get_command_type(self) -> CommandType:
        return CommandType.GET_FREE_TIMETABLE_SLOTS
