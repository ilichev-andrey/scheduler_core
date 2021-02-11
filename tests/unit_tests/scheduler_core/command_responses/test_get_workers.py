import unittest

from ddt import ddt, idata

from command_responses.get_workers import GetWorkersResponse
from database.containers import User, make_user
from database.enums import UserType
from enums import CommandStatus, CommandType


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
        'user_name': 'user_name',
        'phone_number': '8800300600'
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
        # Не удалось загрузить даные в CommandResponse (отсутствует параметр статус)
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
                'workers': [make_user(**worker_data)],
            }
        }
    ]
    for case in cases:
        yield case


@ddt
class TestSummaryResponse(unittest.TestCase):
    @idata(provider_load_from_dict())
    def test_load_from_dict(self, case_data):
        data, expected = case_data['data'], case_data['expected']

        response = GetWorkersResponse()
        self.assertEqual(expected['func_result'], response.load_from_dict(data))
        self.assertEqual(expected['id'], response.id)
        self.assertEqual(expected['status'], response.status)
        self.assertEqual(expected['workers'], response.workers)

    def test_to_dict(self):
        expected = {
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
                'user_name': 'user_name',
                'phone_number': '8800300600'
            }]
        }

        response = GetWorkersResponse()
        response.id = 'command_id'
        response.status = CommandStatus.SUCCESSFUL_EXECUTION
        response.workers = [User(
            id=123,
            type=UserType.WORKER,
            first_name='first_name',
            last_name='last_name',
            user_name='user_name',
            phone_number='8800300600'
        )]
        self.assertEqual(expected, response.to_dict())


if __name__ == '__main__':
    unittest.main()
