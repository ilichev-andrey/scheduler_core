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
        },
        # Успешная загрузка данных при неудачно выполненной команде
        {
            'data': {
                'id': 'command_id',
                'status': {
                    'code': CommandStatus.USER_IS_NOT_FOUND.value,
                    'message': CommandStatus.USER_IS_NOT_FOUND.name
                }
            },
            'expected': {
                'func_result': True,
                'id': 'command_id',
                'status': CommandStatus.USER_IS_NOT_FOUND,
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
            'response': GetUserResponse(
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
        },
        # Неуспешное выполнение команды, не отправляется информация о пользователе
        {
            'response': GetUserResponse(
                command_id='command_id',
                status=CommandStatus.USER_IS_NOT_FOUND
            ),
            'expected': {
                'id': 'command_id',
                'type': CommandType.GET_USER.value,
                'status': {
                    'code': CommandStatus.USER_IS_NOT_FOUND.value,
                    'message': CommandStatus.USER_IS_NOT_FOUND.name
                }
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

        response = GetUserResponse()
        self.assertEqual(expected['func_result'], response.load_from_dict(data))
        self.assertEqual(expected['id'], response.id)
        self.assertEqual(expected['status'], response.status)
        self.assertEqual(expected['user'], response.user)

    @idata(provider_to_dict())
    def test_to_dict(self, case_data):
        response, expected = case_data['response'], case_data['expected']
        self.assertEqual(expected, response.to_dict())


if __name__ == '__main__':
    unittest.main()
