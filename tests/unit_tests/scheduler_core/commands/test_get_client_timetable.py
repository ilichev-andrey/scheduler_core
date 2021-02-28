import unittest

from ddt import ddt, idata

from scheduler_core.commands.get_client_timetable import GetClientTimetableCommand
from scheduler_core.enums import CommandType

COMMAND_ID = ''


def provider_load_from_dict():
    default = GetClientTimetableCommand(command_id=COMMAND_ID)
    failed_result = {
        'func_result': False,
        'id': default.id,
        'client': default.client,
        'limit': default.limit
    }

    cases = [
        # Нет параметра limit
        {
            'data': {'client': 2},
            'expected': failed_result
        },
        # Нет параметра client
        {
            'data': {'limit': 5},
            'expected': failed_result
        },
        # Не удалось загрузить Command, т.к. отсутствует параметр id
        {
            'data': {'client': 2, 'limit': 5},
            'expected': failed_result
        },
        # Успешная загрузка данных
        {
            'data': {
                'id': 'command_id',
                'client': 2,
                'limit': 5
            },
            'expected': {
                'func_result': True,
                'id': 'command_id',
                'client': 2,
                'limit': 5
            }
        }
    ]
    for case in cases:
        yield case


@ddt
class TestGetClientTimetableCommand(unittest.TestCase):
    @idata(provider_load_from_dict())
    def test_load_from_dict(self, case_data):
        data, expected = case_data['data'], case_data['expected']

        command = GetClientTimetableCommand(command_id=COMMAND_ID)
        self.assertEqual(expected['func_result'], command.load_from_dict(data))
        self.assertEqual(expected['id'], command.id)
        self.assertEqual(expected['client'], command.client)
        self.assertEqual(expected['limit'], command.limit)

    def test_to_dict(self):
        expected = {
            'id': 'command_id',
            'type': CommandType.GET_CLIENT_TIMETABLE.value,
            'client': 3,
            'limit': 6
        }

        command = GetClientTimetableCommand()
        command.id = 'command_id'
        command.client = 3
        command.limit = 6
        self.assertEqual(expected, command.to_dict())


if __name__ == '__main__':
    unittest.main()
