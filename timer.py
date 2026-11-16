
import time


class Timer:
    """Таймер для учёта времени выполнения задач."""

    def __init__(self):
        self.start_times = {}
        self.total_times = {}

    def start(self, task_id):
        """Запуск таймера для задачи."""
        if task_id in self.start_times:
            raise ValueError("Таймер уже запущен для этой задачи")

        self.start_times[task_id] = time.monotonic()
        return True

    def stop(self, task_id):
        """Остановка таймера и сохранение времени."""
        if task_id not in self.start_times:
            raise ValueError("Таймер для этой задачи не запущен")

        elapsed = time.monotonic() - self.start_times.pop(task_id)
        self.total_times[task_id] = (
            self.total_times.get(task_id, 0) + elapsed
        )
        return elapsed

    def get_total_time(self, task_id):
        """Получение общего времени выполнения задачи."""
        total = self.total_times.get(task_id, 0)

        if task_id in self.start_times:
            total += time.monotonic() - self.start_times[task_id]

        return total

    def is_running(self, task_id):
        """Проверка состояния таймера."""
        return task_id in self.start_times

    @staticmethod
    def format_time(seconds):
        """Преобразование секунд в часы, минуты и секунды."""
        total_seconds = int(seconds)

        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
