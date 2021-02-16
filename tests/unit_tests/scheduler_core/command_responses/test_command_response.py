import unittest

from ddt import ddt, idata

from scheduler_core.command_responses.command_response import CommandResponse
from scheduler_core.enums import CommandStatus, CommandType


class CommandResponseForTest(CommandResponse):
    def get_command_type(self) -> CommandType:
        return CommandType.UNKNOWN


def provider_load_from_dict():
    default = CommandResponseForTest()
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
                    'code': CommandStatus.SUCCESSFUL_EXECUTION.value,
                    'message': CommandStatus.SUCCESSFUL_EXECUTION.name
                }
            },
            'expected': {
                'func_result': True,
                'id': 'command_id',
                'status': CommandStatus.SUCCESSFUL_EXECUTION
            }
        }
    ]
    for case in cases:
        yield case


@ddt
class TestCommandResponse(unittest.TestCase):
    @idata(provider_load_from_dict())
    def test_load_from_dict(self, case_data):
        data, expected = case_data['data'], case_data['expected']

        response = CommandResponseForTest()
        self.assertEqual(expected['func_result'], response.load_from_dict(data))
        self.assertEqual(expected['id'], response.id)
        self.assertEqual(expected['status'], response.status)

    def test_to_dict(self):
        status = CommandStatus.SUCCESSFUL_EXECUTION
        expected = {
            'id': 'command_id',
            'type': CommandType.UNKNOWN.value,
            'status': {
                'code': status.value,
                'message': status.name
            }
        }

        response = CommandResponseForTest()
        response.id = 'command_id'
        response.status = status
        self.assertEqual(expected, response.to_dict())


if __name__ == '__main__':
    unittest.main()
