import unittest

from ddt import ddt, idata

from scheduler_core.commands.release_timetable_slot import ReleaseTimetableSlotsCommand
from scheduler_core.enums import CommandType

COMMAND_ID = ''


def provider_load_from_dict():
    default = ReleaseTimetableSlotsCommand(command_id=COMMAND_ID)
    failed_result = {
        'func_result': False,
        'id': default.id,
        'timetable_entries': default.timetable_entries
    }

    cases = [
        # Нет параметра timetable_entries
        {
            'data': {},
            'expected': failed_result
        },
        # Тип параметра timetable_entries должен быть List
        {
            'data': {'timetable_entries': 5},
            'expected': failed_result
        },
        # Не удалось загрузить Command, т.к. отсутствует параметр id
        {
            'data': {'timetable_entries': [5]},
            'expected': failed_result
        },
        # Успешная загрузка данных
        {
            'data': {
                'id': 'command_id',
                'timetable_entries': [5]
            },
            'expected': {
                'func_result': True,
                'id': 'command_id',
                'timetable_entries': frozenset((5,))
            }
        }
    ]
    for case in cases:
        yield case


@ddt
class TestReleaseTimetableSlotsCommand(unittest.TestCase):
    @idata(provider_load_from_dict())
    def test_load_from_dict(self, case_data):
        data, expected = case_data['data'], case_data['expected']

        command = ReleaseTimetableSlotsCommand(command_id=COMMAND_ID)
        self.assertEqual(expected['func_result'], command.load_from_dict(data))
        self.assertEqual(expected['id'], command.id)
        self.assertEqual(expected['timetable_entries'], command.timetable_entries)

    def test_to_dict(self):
        expected = {
            'id': 'command_id',
            'type': CommandType.RELEASE_TIMETABLE_SLOTS.value,
            'timetable_entries': [4, 5]
        }

        command = ReleaseTimetableSlotsCommand()
        command.id = 'command_id'
        command.timetable_entries = frozenset((4, 5))
        self.assertEqual(expected, command.to_dict())


if __name__ == '__main__':
    unittest.main()
