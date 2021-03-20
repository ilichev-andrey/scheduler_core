import unittest
from datetime import datetime

from ddt import ddt, idata

from scheduler_core.command_responses.release_timetable_slot import ReleaseTimetableSlotsResponse
from scheduler_core.containers import make_timetable_entry, TimetableEntry
from scheduler_core.enums import CommandStatus, CommandType


def provider_load_from_dict():
    default = ReleaseTimetableSlotsResponse()
    failed_result = {
        'func_result': False,
        'id': default.id,
        'status': default.status,
        'timetable': default.timetable_entries
    }

    timetable_entry = {
        'id': 123,
        'worker_id': 345,
        'client_id': 456,
        'service_id': 567,
        'create_dt': 1614018000,
        'start_dt': 1614070852,
        'end_dt': 1614286852
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
                    'code': CommandStatus.INTERNAL_ERROR.value,
                    'message': CommandStatus.INTERNAL_ERROR.name
                }
            },
            'expected': {
                'func_result': True,
                'id': 'command_id',
                'status': CommandStatus.INTERNAL_ERROR,
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
            'response': ReleaseTimetableSlotsResponse(
                command_id='command_id',
                status=CommandStatus.SUCCESSFUL_EXECUTION,
                timetable_entries=[TimetableEntry(
                    id=123,
                    worker_id=345,
                    client_id=456,
                    service_id=567,
                    service_name='название услуги',
                    create_dt=datetime(2021, 2, 15, 11),
                    start_dt=datetime(2021, 2, 23, 12),
                    end_dt=datetime(2021, 2, 23, 13)
                )]
            ),
            'expected': {
                'id': 'command_id',
                'type': CommandType.RELEASE_TIMETABLE_SLOTS.value,
                'status': {
                    'code': CommandStatus.SUCCESSFUL_EXECUTION.value,
                    'message': CommandStatus.SUCCESSFUL_EXECUTION.name
                },
                'timetable': [{
                    'id': 123,
                    'worker_id': 345,
                    'client_id': 456,
                    'service_id': 567,
                    'service_name': 'название услуги',
                    'create_dt': 1613376000,
                    'start_dt': 1614070800,
                    'end_dt': 1614074400
                }]
            }
        },
        # Неуспешное выполнение команды, не отправляются записи из расписания
        {
            'response': ReleaseTimetableSlotsResponse(
                command_id='command_id',
                status=CommandStatus.INTERNAL_ERROR
            ),
            'expected': {
                'id': 'command_id',
                'type': CommandType.RELEASE_TIMETABLE_SLOTS.value,
                'status': {
                    'code': CommandStatus.INTERNAL_ERROR.value,
                    'message': CommandStatus.INTERNAL_ERROR.name
                }
            }
        }
    ]
    for case in cases:
        yield case


@ddt
class TestReleaseTimetableSlotsResponse(unittest.TestCase):
    @idata(provider_load_from_dict())
    def test_load_from_dict(self, case_data):
        data, expected = case_data['data'], case_data['expected']

        response = ReleaseTimetableSlotsResponse()
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
