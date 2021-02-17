import unittest

from ddt import ddt, idata

from scheduler_core.command_responses.get_services import GetServicesResponse
from scheduler_core.containers import Service, make_service
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
        # Не удалось загрузить данные в CommandResponse (отсутствует параметр статус)
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
                'services': default.services
            }
        }
    ]
    for case in cases:
        yield case


def provider_to_dict():
    cases = [
        # Успешное выполнение команды, отправляются все данные
        {
            'response': GetServicesResponse(
                command_id='command_id',
                status=CommandStatus.SUCCESSFUL_EXECUTION,
                services=[Service(
                    id=123,
                    name='service_name',
                    execution_time_minutes=90
                )]
            ),
            'expected': {
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
        },
        # Неуспешное выполнение команды, не отправляется информация об услугах
        {
            'response': GetServicesResponse(
                command_id='command_id',
                status=CommandStatus.INTERNAL_ERROR
            ),
            'expected': {
                'id': 'command_id',
                'type': CommandType.GET_SERVICES.value,
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
class TestGetServicesResponse(unittest.TestCase):
    @idata(provider_load_from_dict())
    def test_load_from_dict(self, case_data):
        data, expected = case_data['data'], case_data['expected']

        response = GetServicesResponse()
        self.assertEqual(expected['func_result'], response.load_from_dict(data))
        self.assertEqual(expected['id'], response.id)
        self.assertEqual(expected['status'], response.status)
        self.assertEqual(expected['services'], response.services)

    @idata(provider_to_dict())
    def test_to_dict(self, case_data):
        response, expected = case_data['response'], case_data['expected']
        self.assertEqual(expected, response.to_dict())


if __name__ == '__main__':
    unittest.main()
