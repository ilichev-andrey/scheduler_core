import unittest
from datetime import datetime

from ddt import ddt, idata

from scheduler_core.command_responses.get_free_timetable_slots import GetFreeTimetableSlotsResponse
from scheduler_core.containers import make_timetable_entry, TimetableEntry
from scheduler_core.enums import CommandStatus, CommandType


def provider_load_from_dict():
    default = GetFreeTimetableSlotsResponse()
    failed_result = {
        'func_result': False,
        'id': default.id,
        'status': default.status,
        'timetable': default.timetable_entries
    }

    timetable_entry = {
        'id': 123,
        'worker_id': 345,
        'create_dt': 1614018000,
        'start_dt': 1614070852
    }

    cases = [
        # Нет параметра timetable
        {
            'data': {},
            'expected': failed_result
        },
        # Тип параметра timetable должен быть List
        {
            'data': {'timetable': {}},
            'expected': failed_result
        },
        # Не удалось загрузить данные в CommandResponse (отсутствует параметр статус)
        {
            'data': {
                'timetable': [],
                'id': 'command_id'
            },
            'expected': failed_result
        },
        # Успешная загрузка данных
        {
            'data': {
                'id': 'command_id',
                'status': {
                    'code': CommandStatus.SUCCESSFUL_EXECUTION.value,
                    'message': CommandStatus.SUCCESSFUL_EXECUTION.name
                },
                'timetable': [timetable_entry]
            },
            'expected': {
                'func_result': True,
                'id': 'command_id',
                'status': CommandStatus.SUCCESSFUL_EXECUTION,
                'timetable': [make_timetable_entry(**timetable_entry)]
            }
        },
        # Успешная загрузка данных при неудачно выполненной команде
        {
            'data': {
                'id': 'command_id',
                'status': {
                    'code': CommandStatus.NO_FREE_SLOTS_FOUND.value,
                    'message': CommandStatus.NO_FREE_SLOTS_FOUND.name
                }
            },
            'expected': {
                'func_result': True,
                'id': 'command_id',
                'status': CommandStatus.NO_FREE_SLOTS_FOUND,
                'timetable': default.timetable_entries
            }
        }
    ]
    for case in cases:
        yield case


def provider_to_dict():
    cases = [
        # Успешное выполнение команды, отправляются все данные
        {
            'response': GetFreeTimetableSlotsResponse(
                command_id='command_id',
                status=CommandStatus.SUCCESSFUL_EXECUTION,
                timetable_entries=[TimetableEntry(id=123, start_dt=datetime(2021, 2, 23, 12))]
            ),
            'expected': {
                'id': 'command_id',
                'type': CommandType.GET_FREE_TIMETABLE_SLOTS.value,
                'status': {
                    'code': CommandStatus.SUCCESSFUL_EXECUTION.value,
                    'message': CommandStatus.SUCCESSFUL_EXECUTION.name
                },
                'timetable': [{
                    'id': 123,
                    'worker_id': None,
                    'client_id': None,
                    'service_id': None,
                    'service_name': None,
                    'create_dt': None,
                    'start_dt': 1614070800,
                    'end_dt': None
                }]
            }
        },
        # Неуспешное выполнение команды, не отправляются идентификаторы свободных слотов расписания
        {
            'response': GetFreeTimetableSlotsResponse(
                command_id='command_id',
                status=CommandStatus.NO_FREE_SLOTS_FOUND
            ),
            'expected': {
                'id': 'command_id',
                'type': CommandType.GET_FREE_TIMETABLE_SLOTS.value,
                'status': {
                    'code': CommandStatus.NO_FREE_SLOTS_FOUND.value,
                    'message': CommandStatus.NO_FREE_SLOTS_FOUND.name
                }
            }
        }
    ]
    for case in cases:
        yield case


@ddt
class TestGetFreeTimetableSlotsResponse(unittest.TestCase):
    @idata(provider_load_from_dict())
    def test_load_from_dict(self, case_data):
        data, expected = case_data['data'], case_data['expected']

        response = GetFreeTimetableSlotsResponse()
        self.assertEqual(expected['func_result'], response.load_from_dict(data))
        self.assertEqual(expected['id'], response.id)
        self.assertEqual(expected['status'], response.status)
        self.assertEqual(expected['timetable'], response.timetable_entries)

    @idata(provider_to_dict())
    def test_to_dict(self, case_data):
        response, expected = case_data['response'], case_data['expected']
        self.assertEqual(expected, response.to_dict())


if __name__ == '__main__':
    unittest.main()
