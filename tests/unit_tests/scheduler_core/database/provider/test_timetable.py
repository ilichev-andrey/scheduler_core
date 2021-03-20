import collections
import unittest
from datetime import datetime

from scheduler_core import enums, containers
from scheduler_core.database.provider import timetable


class TestFilters(unittest.TestCase):
    def test_filter_entries_by_date(self):
        entries = [
            containers.TimetableEntry(id=1, start_dt=datetime(2021, 3, 19, 15, 30, 20)),
            containers.TimetableEntry(id=1, start_dt=datetime(2021, 3, 20, 15, 30, 19)),
            containers.TimetableEntry(id=1, start_dt=datetime(2021, 3, 20, 15, 30, 20)),
            containers.TimetableEntry(id=1, start_dt=datetime(2021, 3, 20, 15, 30, 21)),
            containers.TimetableEntry(id=1, start_dt=datetime(2021, 3, 21, 15, 30, 20))
        ]

        reference_dt = datetime(2021, 3, 20, 15, 30, 20)
        cases = [
            collections.OrderedDict({
                'entries': entries,
                'time_type': enums.TimeType.PAST,
                'expected': [
                    containers.TimetableEntry(id=1, start_dt=datetime(2021, 3, 19, 15, 30, 20)),
                    containers.TimetableEntry(id=1, start_dt=datetime(2021, 3, 20, 15, 30, 19)),
                    containers.TimetableEntry(id=1, start_dt=datetime(2021, 3, 20, 15, 30, 20))
                ]
            }),
            collections.OrderedDict({
                'entries': entries,
                'time_type': enums.TimeType.FUTURE,
                'expected': [
                    containers.TimetableEntry(id=1, start_dt=datetime(2021, 3, 20, 15, 30, 21)),
                    containers.TimetableEntry(id=1, start_dt=datetime(2021, 3, 21, 15, 30, 20))
                ]
            }),
            collections.OrderedDict({
                'entries': entries,
                'time_type': enums.TimeType.UNKNOWN,
                'expected': []
            })
        ]

        for case in cases:
            entries, time_type, expected = case.values()
            self.assertEqual(expected, timetable._filter_entries_by_date(entries, time_type, reference_dt))


if __name__ == '__main__':
    unittest.main()
