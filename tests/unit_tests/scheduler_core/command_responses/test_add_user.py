import unittest

from ddt import ddt, idata

from scheduler_core.command_responses.add_user import AddUserResponse
from scheduler_core.containers import User
from scheduler_core.enums import CommandStatus, CommandType, UserType


def provider_load_from_dict():
    default = AddUserResponse()
    cases = [
        # Успешная загрузка данных
        {
            'data': {
                'id': 'command_id',
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
            },
            'expected': {
                'func_result': True,
                'id': 'command_id',
                'status': CommandStatus.SUCCESSFUL_EXECUTION,
                'user': User(
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
            }
        },
        # Успешная загрузка данных при неудачно выполненной команде
        {
            'data': {
                'id': 'command_id',
                'status': {
                    'code': CommandStatus.USER_ALREADY_EXISTS.value,
                    'message': CommandStatus.USER_ALREADY_EXISTS.name
                }
            },
            'expected': {
                'func_result': True,
                'id': 'command_id',
                'status': CommandStatus.USER_ALREADY_EXISTS,
                'user': default.user
            }
        }
    ]
    for case in cases:
        yield case


def provider_to_dict():
    cases = [
        # Успешное выполнение команды, отправляются все данные
        {
            'response': AddUserResponse(
                command_id='command_id',
                status=CommandStatus.SUCCESSFUL_EXECUTION,
                user=User(
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
            ),
            'expected': {
                'id': 'command_id',
                'type': CommandType.ADD_USER.value,
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
        },
        # Неуспешное выполнение команды, не отправляется информация о пользователе
        {
            'response': AddUserResponse(
                command_id='command_id',
                status=CommandStatus.USER_ALREADY_EXISTS
            ),
            'expected': {
                'id': 'command_id',
                'type': CommandType.ADD_USER.value,
                'status': {
                    'code': CommandStatus.USER_ALREADY_EXISTS.value,
                    'message': CommandStatus.USER_ALREADY_EXISTS.name
                }
            }
        }
    ]
    for case in cases:
        yield case


@ddt
class TestAddUserResponse(unittest.TestCase):
    @idata(provider_load_from_dict())
    def test_load_from_dict(self, case_data):
        data, expected = case_data['data'], case_data['expected']

        response = AddUserResponse()
        self.assertEqual(expected['func_result'], response.load_from_dict(data))
        self.assertEqual(expected['id'], response.id)
        self.assertEqual(expected['status'], response.status)

    @idata(provider_to_dict())
    def test_to_dict(self, case_data):
        response, expected = case_data['response'], case_data['expected']
        self.assertEqual(expected, response.to_dict())


if __name__ == '__main__':
    unittest.main()
