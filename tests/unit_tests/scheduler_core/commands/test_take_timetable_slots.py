import unittest

from ddt import ddt, idata

from scheduler_core.commands.take_timetable_slots import TakeTimetableSlotsCommand
from scheduler_core.enums import CommandType

COMMAND_ID = ''


def provider_load_from_dict():
    default = TakeTimetableSlotsCommand(command_id=COMMAND_ID)
    failed_result = {
        'func_result': False,
        'id': default.id,
        'timetable_entries': default.timetable_entries,
        'services': default.services,
        'client': default.client
    }

    cases = [
        # Нет параметра timetable_entries
        {
            'data': {'services': [1], 'client': 2},
            'expected': failed_result
        },
        # Нет параметра services
        {
            'data': {'timetable_entries': [5], 'client': 2},
            'expected': failed_result
        },
        # Нет параметра client
        {
            'data': {'timetable_entries': [5], 'services': [1]},
            'expected': failed_result
        },
        # Тип параметра timetable_entries должен быть List
        {
            'data': {'timetable_entries': 5, 'services': [1], 'client': 2},
            'expected': failed_result
        },
        # Тип параметра services должен быть List
        {
            'data': {'timetable_entries': [5], 'services': {1}, 'client': 2},
            'expected': failed_result
        },
        # Не удалось загрузить Command, т.к. отсутствует параметр id
        {
            'data': {'timetable_entries': [5], 'services': [1], 'client': 2},
            'expected': failed_result
        },
        # Успешная загрузка данных
        {
            'data': {
                'id': 'command_id',
                'timetable_entries': [5],
                'services': [1],
                'client': 2
            },
            'expected': {
                'func_result': True,
                'id': 'command_id',
                'timetable_entries': frozenset((5,)),
                'services': frozenset((1,)),
                'client': 2
            }
        }
    ]
    for case in cases:
        yield case


@ddt
class TestTakeTimetableSlotsCommand(unittest.TestCase):
    @idata(provider_load_from_dict())
    def test_load_from_dict(self, case_data):
        data, expected = case_data['data'], case_data['expected']

        command = TakeTimetableSlotsCommand(command_id=COMMAND_ID)
        self.assertEqual(expected['func_result'], command.load_from_dict(data))
        self.assertEqual(expected['id'], command.id)
        self.assertEqual(expected['timetable_entries'], command.timetable_entries)
        self.assertEqual(expected['services'], command.services)
        self.assertEqual(expected['client'], command.client)

    def test_to_dict(self):
        expected = {
            'id': 'command_id',
            'type': CommandType.TAKE_TIMETABLE_SLOTS.value,
            'timetable_entries': [4, 5],
            'services': [1, 2],
            'client': 3
        }

        command = TakeTimetableSlotsCommand()
        command.id = 'command_id'
        command.timetable_entries = frozenset((4, 5))
        command.services = frozenset((1, 2))
        command.client = 3
        self.assertEqual(expected, command.to_dict())


if __name__ == '__main__':
    unittest.main()
