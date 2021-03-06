import unittest

from ddt import ddt, idata

from scheduler_core.commands.update_user import UpdateUserCommand
from scheduler_core.containers import User
from scheduler_core.enums import CommandType, UserType


COMMAND_ID = ''


def provider_load_from_dict():
    default = UpdateUserCommand(command_id=COMMAND_ID)
    failed_result = {
        'func_result': False,
        'id': default.id,
        'user': default.user
    }

    user_data = {
        'id': 6789,
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
                'user': User(
                    id=6789,
                    type=UserType.UNKNOWN,
                    first_name='first_name',
                    last_name='last_name',
                    phone_number='88003000600',
                    telegram_id=12345,
                    telegram_name='telegram_name',
                    viber_id=54321,
                    viber_name='viber_name'
                )
            }
        }
    ]
    for case in cases:
        yield case


@ddt
class TestUpdateUserCommand(unittest.TestCase):
    @idata(provider_load_from_dict())
    def test_load_from_dict(self, case_data):
        data, expected = case_data['data'], case_data['expected']

        command = UpdateUserCommand(command_id=COMMAND_ID)
        self.assertEqual(expected['func_result'], command.load_from_dict(data))
        self.assertEqual(expected['id'], command.id)
        self.assertEqual(expected['user'], command.user)

    def test_to_dict(self):
        expected = {
            'id': 'command_id',
            'type': CommandType.UPDATE_USER.value,
            'user': {
                'id': 6789,
                'first_name': 'first_name',
                'last_name': 'last_name',
                'phone_number': '88003000600',
                'telegram_id': 12345,
                'telegram_name': 'telegram_name',
                'viber_id': 54321,
                'viber_name': 'viber_name'
            }
        }

        command = UpdateUserCommand()
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
