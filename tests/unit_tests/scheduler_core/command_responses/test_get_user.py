import unittest

from ddt import ddt, idata

from scheduler_core.command_responses.get_user import GetUserResponse
from scheduler_core.database.containers import User, make_user
from scheduler_core.database.enums import UserType
from scheduler_core.enums import CommandType, CommandStatus


def provider_load_from_dict():
    default = GetUserResponse()
    failed_result = {
        'func_result': False,
        'id': default.id,
        'status': CommandStatus.UNKNOWN,
        'user': default.user
    }

    user_data = {
        'id': 789,
        'type': UserType.CLIENT.value,
        'first_name': 'first_name',
        'last_name': 'last_name',
        'phone_number': '88003000600',
        'telegram_id': 12345,
        'telegram_name': 'telegram_name',
        'viber_id': 54321,
        'viber_name': 'viber_name'
    }

    cases = [
        # Нет параметра user
        {
            'data': {},
            'expected': failed_result
        },
        # Тип параметра user должен быть Dict
        {
            'data': {'user': []},
            'expected': failed_result
        },
        # Не удалось загрузить Command, т.к. отсутствует параметр id
        {
            'data': {
                'status': {
                    'code': CommandStatus.SUCCESSFUL_EXECUTION.value,
                    'message': CommandStatus.SUCCESSFUL_EXECUTION.name
                },
                'user': user_data
            },
            'expected': failed_result
        },
        # Успешная загрузка данных
        {
            'data': {
                'id': 'command_id',
                'status': {
                    'code': CommandStatus.SUCCESSFUL_EXECUTION.value,
                    'message': CommandStatus.SUCCESSFUL_EXECUTION.name
                },
                'user': user_data
            },
            'expected': {
                'func_result': True,
                'id': 'command_id',
                'status': CommandStatus.SUCCESSFUL_EXECUTION,
                'user': make_user(**user_data)
            }
        }
    ]
    for case in cases:
        yield case


@ddt
class TestGetUserResponse(unittest.TestCase):
    @idata(provider_load_from_dict())
    def test_load_from_dict(self, case_data):
        data, expected = case_data['data'], case_data['expected']

        command = GetUserResponse()
        self.assertEqual(expected['func_result'], command.load_from_dict(data))
        self.assertEqual(expected['id'], command.id)
        self.assertEqual(expected['status'], command.status)
        self.assertEqual(expected['user'], command.user)

    def test_to_dict(self):
        expected = {
            'id': 'command_id',
            'type': CommandType.GET_USER.value,
            'status': {
                'code': CommandStatus.SUCCESSFUL_EXECUTION.value,
                'message': CommandStatus.SUCCESSFUL_EXECUTION.name
            },
            'user': {
                'id': 789,
                'type': UserType.CLIENT.value,
                'first_name': 'first_name',
                'last_name': 'last_name',
                'phone_number': '88003000600',
                'telegram_id': 12345,
                'telegram_name': 'telegram_name',
                'viber_id': 54321,
                'viber_name': 'viber_name'
            }
        }

        command = GetUserResponse()
        command.id = 'command_id'
        command.status = CommandStatus.SUCCESSFUL_EXECUTION
        command.user = User(
            id=789,
            type=UserType.CLIENT,
            first_name='first_name',
            last_name='last_name',
            phone_number='88003000600',
            telegram_id=12345,
            telegram_name='telegram_name',
            viber_id=54321,
            viber_name='viber_name'
        )
        self.assertEqual(expected, command.to_dict())


if __name__ == '__main__':
    unittest.main()
