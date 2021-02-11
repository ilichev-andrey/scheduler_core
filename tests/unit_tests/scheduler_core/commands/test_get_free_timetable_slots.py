import unittest
from datetime import datetime

from ddt import ddt, idata

from commands.get_free_timetable_slots import GetFreeTimetableSlotsCommand
from enums import CommandType


def provider_load_from_dict():
    default = GetFreeTimetableSlotsCommand()
    failed_result = {
        'func_result': False,
        'id': default.id,
        'day': default.day,
        'services': default.services,
        'worker': default.worker
    }

    timestamp = 1612946942
    cases = [
        # Нет параметра day
        {
            'data': {'services': [1], 'worker': 2},
            'expected': failed_result
        },
        # Нет параметра services
        {
            'data': {'day': timestamp, 'worker': 2},
            'expected': failed_result
        },
        # Нет параметра worker
        {
            'data': {'day': timestamp, 'services': [1]},
            'expected': failed_result
        },
        # Тип параметра day должен быть int
        {
            'data': {'day': str(timestamp), 'services': [1], 'worker': 2},
            'expected': failed_result
        },
        # Тип параметра services должен быть List
        {
            'data': {'day': timestamp, 'services': {1}, 'worker': 2},
            'expected': failed_result
        },
        # Не удалось загрузить Command, т.к. отсутствует параметр id
        {
            'data': {'day': timestamp, 'services': [1], 'worker': 2},
            'expected': failed_result
        },
        # Успешная загрузка данных
        {
            'data': {
                'id': 'command_id',
                'day': timestamp,
                'services': [1],
                'worker': 2
            },
            'expected': {
                'func_result': True,
                'id': 'command_id',
                'day': datetime(2021, 2, 10, 11, 49, 2),
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

        command = GetFreeTimetableSlotsCommand()
        self.assertEqual(expected['func_result'], command.load_from_dict(data))
        self.assertEqual(expected['id'], command.id)
        self.assertEqual(expected['day'], command.day)
        self.assertEqual(expected['services'], command.services)
        self.assertEqual(expected['worker'], command.worker)

    def test_to_dict(self):
        expected = {
            'id': 'command_id',
            'type': CommandType.GET_FREE_TIMETABLE_SLOTS.value,
            'day': 1612946942,
            'services': [1, 2],
            'worker': 3
        }

        command = GetFreeTimetableSlotsCommand()
        command.id = 'command_id'
        command.day = datetime(2021, 2, 10, 11, 49, 2)
        command.services = frozenset((1, 2))
        command.worker = 3
        self.assertEqual(expected, command.to_dict())


if __name__ == '__main__':
    unittest.main()
