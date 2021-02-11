import unittest

from ddt import ddt, idata

from commands.get_user import GetUserCommand
from enums import CommandType


def provider_load_from_dict():
    default = GetUserCommand()
    failed_result = {
        'func_result': False,
        'id': default.id,
        'telegram_id': default.telegram_id,
        'viber_id': default.viber_id
    }

    cases = [
        # Нет параметра user
        {
            'data': {},
            'expected': failed_result
        },
        # Нет параметра telegram_id
        {
            'data': {
                'user': {'viber_id': 4321}
            },
            'expected': failed_result
        },
        # Нет параметра viber_id
        {
            'data': {
                'user': {'telegram_id': 1234}
            },
            'expected': failed_result
        },
        # Отсутствуют значения для обоих параметров, должен быть как минимум один
        {
            'data': {
                'user': {'telegram_id': None, 'viber_id': None}
            },
            'expected': failed_result
        },
        # Не удалось загрузить Command, т.к. отсутствует параметр id
        {
            'data': {
                'user': {'telegram_id': 1234, 'viber_id': 4321}
            },
            'expected': failed_result
        },
        # Успешная загрузка данных
        {
            'data': {
                'id': 'command_id',
                'user': {
                    'telegram_id': None,
                    'viber_id': 4321
                }
            },
            'expected': {
                'func_result': True,
                'id': 'command_id',
                'telegram_id': None,
                'viber_id': 4321
            }
        },
        # Успешная загрузка данных
        {
            'data': {
                'id': 'command_id',
                'user': {
                    'telegram_id': 1234,
                    'viber_id': None
                }
            },
            'expected': {
                'func_result': True,
                'id': 'command_id',
                'telegram_id': 1234,
                'viber_id': None
            }
        }
    ]
    for case in cases:
        yield case


@ddt
class TestGetUserCommand(unittest.TestCase):
    @idata(provider_load_from_dict())
    def test_load_from_dict(self, case_data):
        data, expected = case_data['data'], case_data['expected']

        command = GetUserCommand()
        self.assertEqual(expected['func_result'], command.load_from_dict(data))
        self.assertEqual(expected['id'], command.id)
        self.assertEqual(expected['telegram_id'], command.telegram_id)
        self.assertEqual(expected['viber_id'], command.viber_id)

    def test_to_dict(self):
        expected = {
            'id': 'command_id',
            'type': CommandType.GET_USER.value,
            'user': {
                'telegram_id': 1234,
                'viber_id': 4321
            }
        }

        command = GetUserCommand()
        command.id = 'command_id'
        command.telegram_id = 1234
        command.viber_id = 4321
        self.assertEqual(expected, command.to_dict())


if __name__ == '__main__':
    unittest.main()
