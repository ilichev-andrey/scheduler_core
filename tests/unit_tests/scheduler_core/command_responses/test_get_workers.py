import unittest

from ddt import ddt, idata

from scheduler_core.command_responses.get_workers import GetWorkersResponse
from scheduler_core.containers import User
from scheduler_core.enums import CommandStatus, CommandType, UserType


def provider_load_from_dict():
    default = GetWorkersResponse()
    failed_result = {
        'func_result': False,
        'id': default.id,
        'status': default.status,
        'workers': default.workers
    }

    worker_data = {
        'id': 123,
        'type': UserType.WORKER.value,
        'first_name': 'first_name',
        'last_name': 'last_name',
        'phone_number': '8800300600',
        'telegram_id': 456,
        'telegram_name': 'telegram_name',
        'viber_id': 567,
        'viber_name': 'viber_name'
    }

    cases = [
        # Нет параметра workers
        {
            'data': {},
            'expected': failed_result
        },
        # Тип параметра workers должен быть List
        {
            'data': {'workers': {}},
            'expected': failed_result
        },
        # Не удалось загрузить данные в CommandResponse (отсутствует параметр статус)
        {
            'data': {
                'workers': [worker_data],
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
                'workers': [worker_data]
            },
            'expected': {
                'func_result': True,
                'id': 'command_id',
                'status': CommandStatus.SUCCESSFUL_EXECUTION,
                'workers': [User(
                    id=123,
                    type=UserType.WORKER,
                    first_name='first_name',
                    last_name='last_name',
                    phone_number='8800300600',
                    telegram_id=456,
                    telegram_name='telegram_name',
                    viber_id=567,
                    viber_name='viber_name'
                )],
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
                'workers': default.workers
            }
        }
    ]
    for case in cases:
        yield case


def provider_to_dict():
    cases = [
        # Успешное выполнение команды, отправляются все данные
        {
            'response': GetWorkersResponse(
                command_id='command_id',
                status=CommandStatus.SUCCESSFUL_EXECUTION,
                workers=[User(
                    id=123,
                    type=UserType.WORKER,
                    first_name='first_name',
                    last_name='last_name',
                    phone_number='8800300600',
                    telegram_id=456,
                    telegram_name='telegram_name',
                    viber_id=567,
                    viber_name='viber_name'
                )]
            ),
            'expected': {
                'id': 'command_id',
                'type': CommandType.GET_WORKERS.value,
                'status': {
                    'code': CommandStatus.SUCCESSFUL_EXECUTION.value,
                    'message': CommandStatus.SUCCESSFUL_EXECUTION.name
                },
                'workers': [{
                    'id': 123,
                    'type': UserType.WORKER.value,
                    'first_name': 'first_name',
                    'last_name': 'last_name',
                    'phone_number': '8800300600',
                    'telegram_id': 456,
                    'telegram_name': 'telegram_name',
                    'viber_id': 567,
                    'viber_name': 'viber_name'
                }]
            }
        },
        # Неуспешное выполнение команды, не отправляется информация о работниках
        {
            'response': GetWorkersResponse(
                command_id='command_id',
                status=CommandStatus.INTERNAL_ERROR
            ),
            'expected': {
                'id': 'command_id',
                'type': CommandType.GET_WORKERS.value,
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
class TestGetWorkersResponse(unittest.TestCase):
    @idata(provider_load_from_dict())
    def test_load_from_dict(self, case_data):
        data, expected = case_data['data'], case_data['expected']

        response = GetWorkersResponse()
        self.assertEqual(expected['func_result'], response.load_from_dict(data))
        self.assertEqual(expected['id'], response.id)
        self.assertEqual(expected['status'], response.status)
        self.assertEqual(expected['workers'], response.workers)

    @idata(provider_to_dict())
    def test_to_dict(self, case_data):
        response, expected = case_data['response'], case_data['expected']
        self.assertEqual(expected, response.to_dict())


if __name__ == '__main__':
    unittest.main()
