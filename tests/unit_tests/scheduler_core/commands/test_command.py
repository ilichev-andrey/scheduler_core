import unittest

from ddt import ddt, idata

from scheduler_core.commands.command import Command
from scheduler_core.enums import CommandType


class CommandForTest(Command):
    def get_type(self) -> CommandType:
        return CommandType.UNKNOWN


COMMAND_ID = ''


def provider_load_from_dict():
    default = CommandForTest(command_id=COMMAND_ID)
    failed_result = {
        'func_result': False,
        'id': default.id
    }

    cases = [
        # Нет параметра id
        {
            'data': {},
            'expected': failed_result
        },
        # Успешная загрузка данных
        {
            'data': {
                'id': 'command_id'
            },
            'expected': {
                'func_result': True,
                'id': 'command_id'
            }
        }
    ]
    for case in cases:
        yield case


@ddt
class TestCommand(unittest.TestCase):
    @idata(provider_load_from_dict())
    def test_load_from_dict(self, case_data):
        data, expected = case_data['data'], case_data['expected']

        response = CommandForTest(command_id=COMMAND_ID)
        self.assertEqual(expected['func_result'], response.load_from_dict(data))
        self.assertEqual(expected['id'], response.id)

    def test_to_dict(self):
        expected = {
            'id': 'command_id',
            'type': CommandType.UNKNOWN.value
        }

        response = CommandForTest()
        response.id = 'command_id'
        self.assertEqual(expected, response.to_dict())


if __name__ == '__main__':
    unittest.main()
