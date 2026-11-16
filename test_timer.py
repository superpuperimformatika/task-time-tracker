
import unittest
from unittest.mock import patch

from timer import Timer
from task_manager import TaskManager


class TestTimer(unittest.TestCase):
    """Автоматические тесты модуля учёта времени."""

    def setUp(self):
        self.timer = Timer()

    @patch("timer.time.monotonic", side_effect=[100, 110])
    def test_start_stop(self, mock_time):
        """Проверка запуска и остановки таймера."""
        self.timer.start(1)

        self.assertTrue(self.timer.is_running(1))

        elapsed = self.timer.stop(1)

        self.assertEqual(elapsed, 10)
        self.assertFalse(self.timer.is_running(1))
        self.assertEqual(self.timer.get_total_time(1), 10)

    @patch(
        "timer.time.monotonic",
        side_effect=[100, 110, 200, 220]
    )
    def test_multiple_sessions(self, mock_time):
        """Проверка суммирования нескольких сессий."""
        self.timer.start(1)
        self.timer.stop(1)

        self.timer.start(1)
        self.timer.stop(1)

        self.assertEqual(self.timer.get_total_time(1), 30)

    @patch("timer.time.monotonic", return_value=100)
    def test_double_start(self, mock_time):
        """Запрет повторного запуска активного таймера."""
        self.timer.start(1)

        with self.assertRaises(ValueError):
            self.timer.start(1)

    def test_stop_without_start(self):
        """Запрет остановки незапущенного таймера."""
        with self.assertRaises(ValueError):
            self.timer.stop(1)

    def test_format_time(self):
        """Проверка преобразования времени."""
        self.assertEqual(
            Timer.format_time(3661),
            "01:01:01"
        )

    def test_unknown_task(self):
        """Проверка обращения к несуществующей задаче."""
        manager = TaskManager()

        with self.assertRaises(ValueError):
            manager.start_task(999)

    @patch("timer.time.monotonic", side_effect=[100, 115])
    def test_task_manager_integration(self, mock_time):
        """Проверка взаимодействия менеджера и таймера."""
        manager = TaskManager()

        task_id = manager.create_task(
            "Разработка интерфейса",
            "Создание главной страницы"
        )

        manager.start_task(task_id)

        self.assertEqual(
            manager.get_task(task_id)["status"],
            "In Progress"
        )

        manager.stop_task(task_id)

        self.assertEqual(
            manager.get_task_time(task_id),
            15
        )


if __name__ == "__main__":
    unittest.main()
