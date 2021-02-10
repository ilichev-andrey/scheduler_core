import unittest

from ddt import ddt, idata

from command_responses.get_free_timetable_slots import GetFreeTimetableSlotsResponse
from enums import CommandStatus, CommandType


def provider_load_from_dict():
    default = GetFreeTimetableSlotsResponse()
    failed_result = {
        'func_result': False,
        'id': default.id,
        'status': default.status,
        'timetable': default.timetable_ids
    }

    cases = [
        # Нет параметра timetable
        {
            'data': {},
            'expected': failed_result
        },
        # Тип параметра timetable должен быть List
        {
            'data': {'timetable': {1, 2}},
            'expected': failed_result
        },
        # Не удалось загрузить даные в CommandResponse (отсутствует параметр статус)
        {
            'data': {
                'timetable': [1, 2],
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
                'timetable': [1, 2]
            },
            'expected': {
                'func_result': True,
                'id': 'command_id',
                'status': CommandStatus.SUCCESSFUL_EXECUTION,
                'timetable': [1, 2]
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
        self.assertEqual(expected['timetable'], response.timetable_ids)

    def test_to_dict(self):
        expected = {
            'id': 'command_id',
            'type': CommandType.GET_FREE_TIMETABLE_SLOTS.value,
            'status': {
                'code': CommandStatus.SUCCESSFUL_EXECUTION.value,
                'message': CommandStatus.SUCCESSFUL_EXECUTION.name
            },
            'timetable': [123, 456]
        }

        response = GetFreeTimetableSlotsResponse()
        response.id = 'command_id'
        response.status = CommandStatus.SUCCESSFUL_EXECUTION
        response.timetable_ids = [123, 456]
        self.assertEqual(expected, response.to_dict())


if __name__ == '__main__':
    unittest.main()
