
from datetime import datetime
from pathlib import Path


class ReportGenerator:
    """Формирование отчётов по времени выполнения задач."""

    def __init__(self, task_manager):
        self.task_manager = task_manager

    def generate_report(self):
        """Создание текстового отчёта по всем задачам."""
        tasks = self.task_manager.get_all_tasks()

        lines = [
            "ОТЧЁТ ПО УЧЁТУ ВРЕМЕНИ",
            "=" * 45,
            f"Дата формирования: {datetime.now():%d.%m.%Y %H:%M}",
            ""
        ]

        total_seconds = 0

        if not tasks:
            lines.append("Задачи отсутствуют.")

        for task in tasks:
            task_id = task["id"]
            seconds = self.task_manager.get_task_time(task_id)
            total_seconds += seconds

            lines.extend([
                f"ID задачи: {task_id}",
                f"Название: {task['title']}",
                f"Описание: {task['description']}",
                f"Статус: {task['status']}",
                "Затраченное время: "
                + self.task_manager.timer.format_time(seconds),
                "-" * 45
            ])

        lines.extend([
            "",
            f"Всего задач: {len(tasks)}",
            "Общее затраченное время: "
            + self.task_manager.timer.format_time(total_seconds)
        ])

        return "\n".join(lines)

    def save_report(self, filename="time_report.txt"):
        """Сохранение отчёта в текстовый файл."""
        report = self.generate_report()

        Path(filename).write_text(
            report,
            encoding="utf-8"
        )

        return filename
