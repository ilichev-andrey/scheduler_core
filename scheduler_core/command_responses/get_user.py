from scheduler_core.command_responses.response_with_user import ResponseWithUser
from scheduler_core.enums import CommandType


class GetUserResponse(ResponseWithUser):
    def __str__(self):
        return f'GetUserResponse(id={self.id}, status={self.status}, user={self.user})'

    def get_command_type(self) -> CommandType:
        return CommandType.GET_USER
