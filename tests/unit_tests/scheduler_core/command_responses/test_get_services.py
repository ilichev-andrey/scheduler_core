import unittest

from ddt import ddt, idata

from scheduler_core.command_responses.get_services import GetServicesResponse
from scheduler_core.database.containers import Service, make_service
from scheduler_core.enums import CommandStatus, CommandType


def provider_load_from_dict():
    default = GetServicesResponse()
    failed_result = {
        'func_result': False,
        'id': default.id,
        'status': default.status,
        'services': default.services
    }

    service_data = {
        'id': 123,
        'name': 'service_name',
        'execution_time_minutes': 90
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
        # Не удалось загрузить даные в CommandResponse (отсутствует параметр статус)
        {
            'data': {
                'services': [service_data],
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
                'services': [service_data]
            },
            'expected': {
                'func_result': True,
                'id': 'command_id',
                'status': CommandStatus.SUCCESSFUL_EXECUTION,
                'services': [make_service(**service_data)],
            }
        }
    ]
    for case in cases:
        yield case


@ddt
class TestGetServicesResponse(unittest.TestCase):
    @idata(provider_load_from_dict())
    def test_load_from_dict(self, case_data):
        data, expected = case_data['data'], case_data['expected']

        response = GetServicesResponse()
        self.assertEqual(expected['func_result'], response.load_from_dict(data))
        self.assertEqual(expected['id'], response.id)
        self.assertEqual(expected['status'], response.status)
        self.assertEqual(expected['services'], response.services)

    def test_to_dict(self):
        expected = {
            'id': 'command_id',
            'type': CommandType.GET_SERVICES.value,
            'status': {
                'code': CommandStatus.SUCCESSFUL_EXECUTION.value,
                'message': CommandStatus.SUCCESSFUL_EXECUTION.name
            },
            'services': [{
                'id': 123,
                'name': 'service_name',
                'execution_time_minutes': 90
            }]
        }

        response = GetServicesResponse()
        response.id = 'command_id'
        response.status = CommandStatus.SUCCESSFUL_EXECUTION
        response.services = [Service(
            id=123,
            name='service_name',
            execution_time_minutes=90
        )]
        self.assertEqual(expected, response.to_dict())


if __name__ == '__main__':
    unittest.main()
