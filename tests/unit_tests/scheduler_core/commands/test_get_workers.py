import unittest

from ddt import ddt, idata

from scheduler_core.commands.get_workers import GetWorkersCommand
from scheduler_core.enums import CommandType


def provider_load_from_dict():
    cases = [
        # Успешная загрузка данных
        {
            'data': {
                'id': 'command_id'
            },
            'expected': {
                'func_result': True,
                'id': 'command_id'
            }
        }
    ]
    for case in cases:
        yield case


@ddt
class TestGetWorkersCommand(unittest.TestCase):
    @idata(provider_load_from_dict())
    def test_load_from_dict(self, case_data):
        data, expected = case_data['data'], case_data['expected']

        response = GetWorkersCommand()
        self.assertEqual(expected['func_result'], response.load_from_dict(data))
        self.assertEqual(expected['id'], response.id)

    def test_to_dict(self):
        expected = {
            'id': 'command_id',
            'type': CommandType.GET_WORKERS.value
        }

        response = GetWorkersCommand()
        response.id = 'command_id'
        self.assertEqual(expected, response.to_dict())


if __name__ == '__main__':
    unittest.main()
