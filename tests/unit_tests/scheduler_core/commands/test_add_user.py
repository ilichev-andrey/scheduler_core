import unittest

from ddt import ddt, idata

from scheduler_core.commands.add_user import AddUserCommand
from scheduler_core.containers import User, make_user
from scheduler_core.enums import CommandType, UserType


COMMAND_ID = ''


def provider_load_from_dict():
    default = AddUserCommand(command_id=COMMAND_ID)
    failed_result = {
        'func_result': False,
        'id': default.id,
        'user': default.user
    }

    user_data = {
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
            'data': {'user': user_data},
            'expected': failed_result
        },
        # Успешная загрузка данных
        {
            'data': {
                'id': 'command_id',
                'user': user_data
            },
            'expected': {
                'func_result': True,
                'id': 'command_id',
                'user': make_user(id=None, **user_data)
            }
        }
    ]
    for case in cases:
        yield case


@ddt
class TestAddUserCommand(unittest.TestCase):
    @idata(provider_load_from_dict())
    def test_load_from_dict(self, case_data):
        data, expected = case_data['data'], case_data['expected']

        command = AddUserCommand(command_id=COMMAND_ID)
        self.assertEqual(expected['func_result'], command.load_from_dict(data))
        self.assertEqual(expected['id'], command.id)
        self.assertEqual(expected['user'], command.user)

    def test_to_dict(self):
        expected = {
            'id': 'command_id',
            'type': CommandType.ADD_USER.value,
            'user': {
                'first_name': 'first_name',
                'last_name': 'last_name',
                'phone_number': '88003000600',
                'telegram_id': 12345,
                'telegram_name': 'telegram_name',
                'viber_id': 54321,
                'viber_name': 'viber_name'
            }
        }

        command = AddUserCommand()
        command.id = 'command_id'
        command.user = User(
            id=6789,
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
