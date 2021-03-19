import unittest
from datetime import datetime

from scheduler_core.command_executors import get_worker_timetable
from scheduler_core.containers import DateRanges
from scheduler_core.enums import TimeLimit, TimeType


class TestGetDataRanges(unittest.TestCase):
    def test_get_data_ranges(self):
        today = datetime(2021, 3, 3).date()
        cases = [
            [
                {'time_type': TimeType.PAST, 'time_limit': TimeLimit.DAY},
                DateRanges(start_dt=datetime(2021, 3, 3, 0, 0, 0), end_dt=datetime(2021, 3, 3, 23, 59, 59)),
            ],
            [
                {'time_type': TimeType.PAST, 'time_limit': TimeLimit.WEEK},
                DateRanges(start_dt=datetime(2021, 2, 25, 0, 0, 0), end_dt=datetime(2021, 3, 3, 23, 59, 59)),
            ],
            [
                {'time_type': TimeType.PAST, 'time_limit': TimeLimit.MONTH},
                DateRanges(start_dt=datetime(2021, 2, 2, 0, 0, 0), end_dt=datetime(2021, 3, 3, 23, 59, 59)),
            ],
            [
                {'time_type': TimeType.PAST, 'time_limit': TimeLimit.NO_LIMIT},
                DateRanges(start_dt=datetime(2020, 1, 1, 0, 0, 0), end_dt=datetime(2021, 3, 3, 23, 59, 59)),
            ],
            [
                {'time_type': TimeType.FUTURE, 'time_limit': TimeLimit.DAY},
                DateRanges(start_dt=datetime(2021, 3, 3, 0, 0, 0), end_dt=datetime(2021, 3, 3, 23, 59, 59)),
            ],
            [
                {'time_type': TimeType.FUTURE, 'time_limit': TimeLimit.WEEK},
                DateRanges(start_dt=datetime(2021, 3, 3, 0, 0, 0), end_dt=datetime(2021, 3, 9, 23, 59, 59)),
            ],
            [
                {'time_type': TimeType.FUTURE, 'time_limit': TimeLimit.MONTH},
                DateRanges(start_dt=datetime(2021, 3, 3, 0, 0, 0), end_dt=datetime(2021, 4, 1, 23, 59, 59)),
            ],
            [
                {'time_type': TimeType.FUTURE, 'time_limit': TimeLimit.NO_LIMIT},
                DateRanges(start_dt=datetime(2021, 3, 3, 0, 0, 0)),
            ]
        ]
        for _params, _expected in cases:
            self.assertEqual(_expected, get_worker_timetable._get_data_ranges(today=today, **_params))


if __name__ == '__main__':
    unittest.main()
