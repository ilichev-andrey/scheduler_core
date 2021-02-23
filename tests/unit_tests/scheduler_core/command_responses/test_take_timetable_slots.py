import unittest

from ddt import ddt, idata

from scheduler_core.command_responses.take_timetable_slots import TakeTimetableSlotsResponse
from scheduler_core.enums import CommandStatus, CommandType


def provider_load_from_dict():
    cases = [
        # Успешная загрузка данных
        {
            'data': {
                'id': 'command_id',
                'status': {
                    'code': CommandStatus.SUCCESSFUL_EXECUTION.value,
                    'message': CommandStatus.SUCCESSFUL_EXECUTION.name
                }
            },
            'expected': {
                'func_result': True,
                'id': 'command_id',
                'status': CommandStatus.SUCCESSFUL_EXECUTION
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
                'status': CommandStatus.INTERNAL_ERROR
            }
        }
    ]
    for case in cases:
        yield case


def provider_to_dict():
    cases = [
        # Успешное выполнение команды, отправляются все данные
        {
            'response': TakeTimetableSlotsResponse(
                command_id='command_id',
                status=CommandStatus.SUCCESSFUL_EXECUTION
            ),
            'expected': {
                'id': 'command_id',
                'type': CommandType.TAKE_TIMETABLE_SLOTS.value,
                'status': {
                    'code': CommandStatus.SUCCESSFUL_EXECUTION.value,
                    'message': CommandStatus.SUCCESSFUL_EXECUTION.name
                }
            }
        },
        # Неуспешное выполнение команды, не отправляется информация об услугах
        {
            'response': TakeTimetableSlotsResponse(
                command_id='command_id',
                status=CommandStatus.SLOT_ALREADY_BUSY
            ),
            'expected': {
                'id': 'command_id',
                'type': CommandType.TAKE_TIMETABLE_SLOTS.value,
                'status': {
                    'code': CommandStatus.SLOT_ALREADY_BUSY.value,
                    'message': CommandStatus.SLOT_ALREADY_BUSY.name
                }
            }
        }
    ]
    for case in cases:
        yield case


@ddt
class TestTakeTimetableSlotsResponse(unittest.TestCase):
    @idata(provider_load_from_dict())
    def test_load_from_dict(self, case_data):
        data, expected = case_data['data'], case_data['expected']

        response = TakeTimetableSlotsResponse()
        self.assertEqual(expected['func_result'], response.load_from_dict(data))
        self.assertEqual(expected['id'], response.id)
        self.assertEqual(expected['status'], response.status)

    @idata(provider_to_dict())
    def test_to_dict(self, case_data):
        response, expected = case_data['response'], case_data['expected']
        self.assertEqual(expected, response.to_dict())


if __name__ == '__main__':
    unittest.main()
