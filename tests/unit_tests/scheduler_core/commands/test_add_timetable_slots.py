import unittest
from datetime import datetime, time

from ddt import ddt, idata

from scheduler_core.commands.add_timetable_slots import AddTimetableSlotsCommand
from scheduler_core.containers import DateRanges
from scheduler_core.enums import CommandType

COMMAND_ID = ''


def provider_load_from_dict():
    default = AddTimetableSlotsCommand(command_id=COMMAND_ID)
    failed_result = {
        'func_result': False,
        'id': default.id,
        'date_ranges': default.date_ranges,
        'times': default.times,
        'worker': default.worker
    }

    date_ranges = {
        'start_dt': 1612946942,
        'end_dt': 1615323600
    }

    cases = [
        # Нет параметра date_ranges
        {
            'data': {'times': ['10:30'], 'worker': 2},
            'expected': failed_result
        },
        # Нет параметра times
        {
            'data': {'date_ranges': date_ranges, 'worker': 2},
            'expected': failed_result
        },
        # Нет параметра worker
        {
            'data': {'date_ranges': date_ranges, 'times': ['10:30']},
            'expected': failed_result
        },
        # Тип параметра date_ranges должен быть int
        {
            'data': {'date_ranges': str(1234), 'times': ['10:30'], 'worker': 2},
            'expected': failed_result
        },
        # Тип параметра times должен быть List
        {
            'data': {'date_ranges': date_ranges, 'times': {'10:30'}, 'worker': 2},
            'expected': failed_result
        },
        # Не удалось загрузить Command, т.к. отсутствует параметр id
        {
            'data': {'date_ranges': date_ranges, 'times': ['10:30'], 'worker': 2},
            'expected': failed_result
        },
        # Успешная загрузка данных
        {
            'data': {
                'id': 'command_id',
                'date_ranges': date_ranges,
                'times': ['10:30'],
                'worker': 2
            },
            'expected': {
                'func_result': True,
                'id': 'command_id',
                'date_ranges': DateRanges(start_dt=datetime(2021, 2, 10, 11, 49, 2), end_dt=datetime(2021, 3, 10)),
                'times': [time(10, 30)],
                'worker': 2
            }
        }
    ]
    for case in cases:
        yield case


@ddt
class TestAddTimetableSlotsCommand(unittest.TestCase):
    @idata(provider_load_from_dict())
    def test_load_from_dict(self, case_data):
        data, expected = case_data['data'], case_data['expected']

        command = AddTimetableSlotsCommand(command_id=COMMAND_ID)
        self.assertEqual(expected['func_result'], command.load_from_dict(data))
        self.assertEqual(expected['id'], command.id)
        self.assertEqual(expected['date_ranges'], command.date_ranges)
        self.assertEqual(expected['times'], command.times)
        self.assertEqual(expected['worker'], command.worker)

    def test_to_dict(self):
        expected = {
            'id': 'command_id',
            'type': CommandType.ADD_TIMETABLE_SLOTS.value,
            'date_ranges': {
                'start_dt': 1612946942,
                'end_dt': 1615323600
            },
            'times': ['10:30', '13:45'],
            'worker': 3
        }

        command = AddTimetableSlotsCommand()
        command.id = 'command_id'
        command.date_ranges = DateRanges(start_dt=datetime(2021, 2, 10, 11, 49, 2), end_dt=datetime(2021, 3, 10))
        command.times = [time(10, 30), time(13, 45)]
        command.worker = 3
        self.assertEqual(expected, command.to_dict())


if __name__ == '__main__':
    unittest.main()
