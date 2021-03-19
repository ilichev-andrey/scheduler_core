import unittest
from collections import OrderedDict
from datetime import datetime, time, date

from scheduler_core.command_executors import add_timetable_slots
from scheduler_core.containers import DateRanges


class TestHandleDateRanges(unittest.TestCase):
    def test_restore_date_order(self):
        # Тестирование функции, которая приводит диапазон дат к правильному порядку

        cases = [
            [
                DateRanges(start_dt=datetime(2021, 3, 20), end_dt=datetime(2021, 3, 19)),
                DateRanges(start_dt=datetime(2021, 3, 19), end_dt=datetime(2021, 3, 20))
            ],
            [
                DateRanges(start_dt=datetime(2021, 2, 20), end_dt=datetime(2021, 1, 30)),
                DateRanges(start_dt=datetime(2021, 1, 30), end_dt=datetime(2021, 2, 20))
            ],
            [
                DateRanges(start_dt=datetime(2021, 3, 20, 12, 30, 59), end_dt=datetime(2021, 3, 20, 12, 30, 58)),
                DateRanges(start_dt=datetime(2021, 3, 20, 12, 30, 58), end_dt=datetime(2021, 3, 20, 12, 30, 59))
            ],
            [
                DateRanges(start_dt=datetime(2021, 3, 20, 12, 30, 58), end_dt=datetime(2021, 3, 20, 12, 30, 59)),
                DateRanges(start_dt=datetime(2021, 3, 20, 12, 30, 58), end_dt=datetime(2021, 3, 20, 12, 30, 59))
            ]
        ]

        for date_ranges, expected in cases:
            self.assertEqual(expected, add_timetable_slots._restore_date_order(date_ranges))

    def test_generate_start_dts(self):
        # Тестирование функции, которая генерирует время начала слота в расписании
        # исходя из диапазона дат и списка времени

        cases = [
            OrderedDict({
                'date_ranges': DateRanges(start_dt=datetime(2021, 3, 20), end_dt=datetime(2021, 3, 23)),
                'times': [time(10, 15), time(12, 50), time(18, 5)],
                'exclude_days': [date(2021, 3, 21), date(2021, 3, 22), date(2021, 3, 24)],
                'expected': [
                    datetime(2021, 3, 20, 10, 15),
                    datetime(2021, 3, 20, 12, 50),
                    datetime(2021, 3, 20, 18, 5),
                    datetime(2021, 3, 23, 10, 15),
                    datetime(2021, 3, 23, 12, 50),
                    datetime(2021, 3, 23, 18, 5)
                ]
            })
        ]

        for case in cases:
            date_ranges, times, exclude_days, expected = case.values()
            self.assertEqual(expected, add_timetable_slots._generate_start_dts(
                date_ranges=date_ranges,
                times=times,
                exclude_days=exclude_days
            ))


if __name__ == '__main__':
    unittest.main()
