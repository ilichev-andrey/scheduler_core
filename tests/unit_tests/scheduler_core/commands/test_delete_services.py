import unittest

from ddt import ddt, idata

from scheduler_core.commands.delete_services import DeleteServicesCommand
from scheduler_core.enums import CommandType

COMMAND_ID = ''


def provider_load_from_dict():
    default = DeleteServicesCommand(command_id=COMMAND_ID)
    failed_result = {
        'func_result': False,
        'id': default.id,
        'services': default.services
    }
    cases = [
        # Нет параметра services
        {
            'data': {'id': 'command_id'},
            'expected': failed_result
        },
        # Тип параметра services должен быть List
        {
            'data': {'services': {1, 2}},
            'expected': failed_result
        },
        # Не удалось загрузить Command, т.к. отсутствует параметр id
        {
            'data': {'services': [1, 2]},
            'expected': failed_result
        },
        # Успешная загрузка данных
        {
            'data': {
                'id': 'command_id',
                'services': [1, 2]
            },
            'expected': {
                'func_result': True,
                'id': 'command_id',
                'services': frozenset((1, 2))
            }
        }
    ]
    for case in cases:
        yield case


@ddt
class TestDeleteServicesCommand(unittest.TestCase):
    @idata(provider_load_from_dict())
    def test_load_from_dict(self, case_data):
        data, expected = case_data['data'], case_data['expected']

        command = DeleteServicesCommand(command_id=COMMAND_ID)
        self.assertEqual(expected['func_result'], command.load_from_dict(data))
        self.assertEqual(expected['id'], command.id)
        self.assertEqual(expected['services'], command.services)

    def test_to_dict(self):
        expected = {
            'id': 'command_id',
            'type': CommandType.DELETE_SERVICES.value,
            'services': [1, 2]
        }

        command = DeleteServicesCommand()
        command.id = 'command_id'
        command.services = frozenset((1, 2))
        self.assertEqual(expected, command.to_dict())


if __name__ == '__main__':
    unittest.main()
