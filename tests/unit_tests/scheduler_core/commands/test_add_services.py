import unittest

from ddt import ddt, idata

from commands.add_services import AddServicesCommand
from database.containers import make_service, Service
from enums import CommandType


def provider_load_from_dict():
    default = AddServicesCommand()
    failed_result = {
        'func_result': False,
        'id': default.id,
        'services': default.services
    }

    service_data = {
        'name': 'service_name',
        'execution_time_minutes': 30
    }

    cases = [
        # Нет параметра services
        {
            'data': {},
            'expected': failed_result
        },
        # Тип параметра services должен быть List
        {
            'data': {'services': {}},
            'expected': failed_result
        },
        # Не удалось загрузить Command, т.к. отсутствует параметр id
        {
            'data': {'services': [service_data]},
            'expected': failed_result
        },
        # Успешная загрузка данных
        {
            'data': {
                'id': 'command_id',
                'services': [service_data]
            },
            'expected': {
                'func_result': True,
                'id': 'command_id',
                'services': [make_service(id=None, **service_data)]
            }
        }
    ]
    for case in cases:
        yield case


@ddt
class TestAddServicesCommand(unittest.TestCase):
    @idata(provider_load_from_dict())
    def test_load_from_dict(self, case_data):
        data, expected = case_data['data'], case_data['expected']

        command = AddServicesCommand()
        self.assertEqual(expected['func_result'], command.load_from_dict(data))
        self.assertEqual(expected['id'], command.id)
        self.assertEqual(expected['services'], command.services)

    def test_to_dict(self):
        expected = {
            'id': 'command_id',
            'type': CommandType.ADD_SERVICES.value,
            'services': [{
                'name': 'service_name',
                'execution_time_minutes': 30
            }]
        }

        command = AddServicesCommand()
        command.id = 'command_id'
        command.services = [Service(id=None, name='service_name', execution_time_minutes=30)]
        self.assertEqual(expected, command.to_dict())


if __name__ == '__main__':
    unittest.main()
