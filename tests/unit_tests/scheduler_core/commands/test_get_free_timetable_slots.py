import unittest
from datetime import datetime

from ddt import ddt, idata

from scheduler_core.commands.get_free_timetable_slots import GetFreeTimetableSlotsCommand
from scheduler_core.containers import DateRanges
from scheduler_core.enums import CommandType

COMMAND_ID = ''


def provider_load_from_dict():
    default = GetFreeTimetableSlotsCommand(command_id=COMMAND_ID)
    failed_result = {
        'func_result': False,
        'id': default.id,
        'date_ranges': default.date_ranges,
        'services': default.services,
        'worker': default.worker
    }

    date_ranges = {
        'start_dt': 1612946942,
        'end_dt': 1615323600
    }

    cases = [
        # Нет параметра day
        {
            'data': {'services': [1], 'worker': 2},
            'expected': failed_result
        },
        # Нет параметра services
        {
            'data': {'date_ranges': date_ranges, 'worker': 2},
            'expected': failed_result
        },
        # Нет параметра worker
        {
            'data': {'date_ranges': date_ranges, 'services': [1]},
            'expected': failed_result
        },
        # Тип параметра day должен быть int
        {
            'data': {'date_ranges': str(1234), 'services': [1], 'worker': 2},
            'expected': failed_result
        },
        # Тип параметра services должен быть List
        {
            'data': {'date_ranges': date_ranges, 'services': {1}, 'worker': 2},
            'expected': failed_result
        },
        # Не удалось загрузить Command, т.к. отсутствует параметр id
        {
            'data': {'date_ranges': date_ranges, 'services': [1], 'worker': 2},
            'expected': failed_result
        },
        # Успешная загрузка данных
        {
            'data': {
                'id': 'command_id',
                'date_ranges': date_ranges,
                'services': [1],
                'worker': 2
            },
            'expected': {
                'func_result': True,
                'id': 'command_id',
                'date_ranges': DateRanges(start_dt=datetime(2021, 2, 10, 11, 49, 2), end_dt=datetime(2021, 3, 10)),
                'services': frozenset((1,)),
                'worker': 2
            }
        }
    ]
    for case in cases:
        yield case


@ddt
class TestGetFreeTimetableSlotsCommand(unittest.TestCase):
    @idata(provider_load_from_dict())
    def test_load_from_dict(self, case_data):
        data, expected = case_data['data'], case_data['expected']

        command = GetFreeTimetableSlotsCommand(command_id=COMMAND_ID)
        self.assertEqual(expected['func_result'], command.load_from_dict(data))
        self.assertEqual(expected['id'], command.id)
        self.assertEqual(expected['date_ranges'], command.date_ranges)
        self.assertEqual(expected['services'], command.services)
        self.assertEqual(expected['worker'], command.worker)

    def test_to_dict(self):
        expected = {
            'id': 'command_id',
            'type': CommandType.GET_FREE_TIMETABLE_SLOTS.value,
            'date_ranges': {
                'start_dt': 1612946942,
                'end_dt': 1615323600
            },
            'services': [1, 2],
            'worker': 3
        }

        command = GetFreeTimetableSlotsCommand()
        command.id = 'command_id'
        command.date_ranges = DateRanges(start_dt=datetime(2021, 2, 10, 11, 49, 2), end_dt=datetime(2021, 3, 10))
        command.services = frozenset((1, 2))
        command.worker = 3
        self.assertEqual(expected, command.to_dict())


if __name__ == '__main__':
    unittest.main()
