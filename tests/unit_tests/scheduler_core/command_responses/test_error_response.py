import unittest

from ddt import ddt, idata

from scheduler_core.command_responses.error_response import ErrorResponse
from scheduler_core.enums import CommandStatus, CommandType


def provider_load_from_dict():
    default = ErrorResponse()
    failed_result = {
        'func_result': False,
        'id': default.id,
        'status': default.status
    }

    cases = [
        # Нет параметра id
        {
            'data': {'status': {}},
            'expected': failed_result
        },
        # Нет параметра status
        {
            'data': {'id': 'command_id'},
            'expected': failed_result
        },
        # Нет параметра code
        {
            'data': {
                'id': 'command_id',
                'status': {
                    'message': CommandStatus.SUCCESSFUL_EXECUTION.name
                }
            },
            'expected': failed_result
        },
        # Успешная загрузка данных
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


@ddt
class TestErrorResponse(unittest.TestCase):
    @idata(provider_load_from_dict())
    def test_load_from_dict(self, case_data):
        data, expected = case_data['data'], case_data['expected']

        response = ErrorResponse()
        self.assertEqual(expected['func_result'], response.load_from_dict(data))
        self.assertEqual(expected['id'], response.id)
        self.assertEqual(expected['status'], response.status)

    def test_to_dict(self):
        status = CommandStatus.INTERNAL_ERROR
        expected = {
            'id': 'command_id',
            'type': CommandType.UNKNOWN.value,
            'status': {
                'code': status.value,
                'message': status.name
            }
        }

        response = ErrorResponse()
        response.id = 'command_id'
        response.status = status
        self.assertEqual(expected, response.to_dict())


if __name__ == '__main__':
    unittest.main()
