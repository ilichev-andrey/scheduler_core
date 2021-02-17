import unittest
from datetime import datetime

from scheduler_core.command_executors import get_free_timetable_slots
from scheduler_core.containers import TimetableEntry


class TestFilterSlotsByExecutionTime(unittest.TestCase):
    @staticmethod
    def _create_slot(entry_id, worker_id, start_dt, is_busy):
        return TimetableEntry(
            id=entry_id,
            worker_id=worker_id,
            client_id=321 if is_busy else None,
            start_dt=start_dt
        )

    def test_filter_slots_by_execution_time(self):
        # Поиск слотов, в которое уложится время выполнения равное 2 часам

        execution_time_minutes = 120
        slots = [
            self._create_slot(entry_id=1, worker_id=1234, start_dt=datetime(2021, 3, 10, 10), is_busy=False),
            self._create_slot(entry_id=2, worker_id=1234, start_dt=datetime(2021, 3, 10, 11, 59), is_busy=True),
            self._create_slot(entry_id=3, worker_id=1234, start_dt=datetime(2021, 3, 10, 13), is_busy=False),
            self._create_slot(entry_id=4, worker_id=1234, start_dt=datetime(2021, 3, 10, 15), is_busy=False),
            self._create_slot(entry_id=5, worker_id=1234, start_dt=datetime(2021, 3, 10, 17, 30), is_busy=False)
        ]
        expected = [
            self._create_slot(entry_id=3, worker_id=1234, start_dt=datetime(2021, 3, 10, 13), is_busy=False),
            self._create_slot(entry_id=4, worker_id=1234, start_dt=datetime(2021, 3, 10, 15), is_busy=False),
            self._create_slot(entry_id=5, worker_id=1234, start_dt=datetime(2021, 3, 10, 17, 30), is_busy=False)
        ]

        self.assertEqual(
            expected,
            get_free_timetable_slots._filter_slots_by_execution_time(slots, execution_time_minutes)
        )


if __name__ == '__main__':
    unittest.main()
