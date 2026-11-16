
import unittest
import tempfile
from pathlib import Path
from unittest.mock import patch

from task_manager import TaskManager
from reports import ReportGenerator


class TestReports(unittest.TestCase):
    """Тестирование формирования отчётов."""

    def setUp(self):
        self.manager = TaskManager()
        self.reports = ReportGenerator(self.manager)

    def test_empty_report(self):
        """Проверка отчёта при отсутствии задач."""
        report = self.reports.generate_report()

        self.assertIn("Задачи отсутствуют", report)
        self.assertIn("Всего задач: 0", report)

    def test_report_with_task(self):
        """Проверка отображения задачи в отчёте."""
        self.manager.create_task(
            "Разработка интерфейса",
            "Создание главной страницы"
        )

        report = self.reports.generate_report()

        self.assertIn("Разработка интерфейса", report)
        self.assertIn("Создание главной страницы", report)
        self.assertIn("To Do", report)
        self.assertIn("Всего задач: 1", report)

    @patch("timer.time.monotonic", side_effect=[100, 160])
    def test_report_total_time(self, mock_time):
        """Проверка подсчёта времени в отчёте."""
        task_id = self.manager.create_task(
            "Тестирование системы"
        )

        self.manager.start_task(task_id)
        self.manager.stop_task(task_id)

        report = self.reports.generate_report()

        self.assertIn(
            "Затраченное время: 00:01:00",
            report
        )
        self.assertIn(
            "Общее затраченное время: 00:01:00",
            report
        )

    def test_save_report(self):
        """Проверка сохранения отчёта в TXT-файл."""
        self.manager.create_task("Подготовка документации")

        with tempfile.TemporaryDirectory() as temp_dir:
            filename = Path(temp_dir) / "report.txt"

            result = self.reports.save_report(filename)

            self.assertEqual(result, filename)
            self.assertTrue(filename.exists())

            content = filename.read_text(encoding="utf-8")

            self.assertIn(
                "Подготовка документации",
                content
            )
            self.assertIn("Всего задач: 1", content)

    def test_multiple_tasks(self):
        """Проверка отчёта по нескольким задачам."""
        self.manager.create_task("Задача 1")
        self.manager.create_task("Задача 2")
        self.manager.create_task("Задача 3")

        report = self.reports.generate_report()

        self.assertIn("Всего задач: 3", report)
        self.assertIn("Задача 1", report)
        self.assertIn("Задача 2", report)
        self.assertIn("Задача 3", report)


if __name__ == "__main__":
    unittest.main()
