import unittest

from ddt import ddt, idata

from scheduler_core.commands.get_worker_timetable import GetWorkerTimetableCommand
from scheduler_core.enums import CommandType, TimeType, TimeLimit

COMMAND_ID = ''


def provider_load_from_dict():
    default = GetWorkerTimetableCommand(command_id=COMMAND_ID)
    failed_result = {
        'func_result': False,
        'id': default.id,
        'worker': default.worker,
        'time_type': default.time_type,
        'time_limit': default.time_limit
    }

    cases = [
        # Нет параметра worker
        {
            'data': {'time_type': TimeType.PAST.value, 'time_limit': TimeLimit.DAY.value},
            'expected': failed_result
        },
        # Нет параметра time_type
        {
            'data': {'worker': 2, 'time_limit': TimeLimit.DAY.value},
            'expected': failed_result
        },
        # Нет параметра time_limit
        {
            'data': {'worker': 2, 'time_type': TimeType.PAST.value},
            'expected': failed_result
        },
        # Не удалось загрузить Command, т.к. отсутствует параметр id
        {
            'data': {'worker': 2, 'time_type': TimeType.PAST.value, 'time_limit': TimeLimit.DAY.value},
            'expected': failed_result
        },
        # Успешная загрузка данных
        {
            'data': {
                'id': 'command_id',
                'worker': 2,
                'time_type': TimeType.PAST.value,
                'time_limit': TimeLimit.DAY.value
            },
            'expected': {
                'func_result': True,
                'id': 'command_id',
                'worker': 2,
                'time_type': TimeType.PAST,
                'time_limit': TimeLimit.DAY
            }
        }
    ]
    for case in cases:
        yield case


@ddt
class TestGetClientTimetableCommand(unittest.TestCase):
    @idata(provider_load_from_dict())
    def test_load_from_dict(self, case_data):
        data, expected = case_data['data'], case_data['expected']

        command = GetWorkerTimetableCommand(command_id=COMMAND_ID)
        self.assertEqual(expected['func_result'], command.load_from_dict(data))
        self.assertEqual(expected['id'], command.id)
        self.assertEqual(expected['worker'], command.worker)
        self.assertEqual(expected['time_type'], command.time_type)
        self.assertEqual(expected['time_limit'], command.time_limit)

    def test_to_dict(self):
        expected = {
            'id': 'command_id',
            'type': CommandType.GET_WORKER_TIMETABLE.value,
            'worker': 3,
            'time_type': TimeType.PAST.value,
            'time_limit': TimeLimit.DAY.value
        }

        command = GetWorkerTimetableCommand()
        command.id = 'command_id'
        command.worker = 3
        command.time_type = TimeType.PAST
        command.time_limit = TimeLimit.DAY
        self.assertEqual(expected, command.to_dict())


if __name__ == '__main__':
    unittest.main()
