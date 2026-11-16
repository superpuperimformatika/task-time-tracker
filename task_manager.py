
from datetime import datetime
from timer import Timer


class TaskManager:
    """Система управления задачами с учётом времени."""

    def __init__(self):
        self.tasks = {}
        self.next_id = 1
        self.timer = Timer()

    def create_task(self, title, description=""):
        """Создание новой задачи."""
        if not title.strip():
            raise ValueError("Название задачи не может быть пустым")

        task_id = self.next_id
        self.tasks[task_id] = {
            "id": task_id,
            "title": title,
            "description": description,
            "status": "To Do",
            "created_at": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        }

        self.next_id += 1
        return task_id

    def get_task(self, task_id):
        """Получение задачи по идентификатору."""
        if task_id not in self.tasks:
            raise ValueError("Задача не найдена")

        return self.tasks[task_id]

    def get_all_tasks(self):
        """Получение списка всех задач."""
        return list(self.tasks.values())

    def update_status(self, task_id, status):
        """Изменение статуса задачи."""
        allowed_statuses = ["To Do", "In Progress", "Done"]

        if status not in allowed_statuses:
            raise ValueError("Недопустимый статус задачи")

        task = self.get_task(task_id)
        task["status"] = status

    def start_task(self, task_id):
        """Запуск таймера выбранной задачи."""
        task = self.get_task(task_id)

        if task["status"] == "Done":
            raise ValueError("Завершённую задачу нельзя запустить")

        self.timer.start(task_id)
        task["status"] = "In Progress"

    def stop_task(self, task_id):
        """Остановка таймера задачи."""
        self.get_task(task_id)
        return self.timer.stop(task_id)

    def get_task_time(self, task_id):
        """Получение затраченного времени."""
        self.get_task(task_id)
        return self.timer.get_total_time(task_id)

    def complete_task(self, task_id):
        """Завершение задачи."""
        task = self.get_task(task_id)

        if self.timer.is_running(task_id):
            self.timer.stop(task_id)

        task["status"] = "Done"
