
from task_manager import TaskManager
from reports import ReportGenerator


def main():
    """Главное меню системы учёта времени."""
    manager = TaskManager()
    reports = ReportGenerator(manager)

    while True:
        print("\n===== СИСТЕМА УЧЁТА ВРЕМЕНИ =====")
        print("1. Создать задачу")
        print("2. Просмотреть задачи")
        print("3. Запустить таймер")
        print("4. Остановить таймер")
        print("5. Посмотреть затраченное время")
        print("6. Изменить статус задачи")
        print("7. Завершить задачу")
        print("8. Сформировать отчёт")
        print("9. Сохранить отчёт в файл")
        print("0. Выход")

        choice = input("\nВыберите действие: ").strip()

        try:
            if choice == "1":
                title = input("Название задачи: ")
                description = input("Описание задачи: ")

                task_id = manager.create_task(title, description)
                print(f"Задача создана! ID: {task_id}")

            elif choice == "2":
                tasks = manager.get_all_tasks()

                if not tasks:
                    print("Список задач пуст.")

                for task in tasks:
                    print(
                        f"ID: {task['id']} | "
                        f"Название: {task['title']} | "
                        f"Статус: {task['status']}"
                    )

            elif choice == "3":
                task_id = int(input("Введите ID задачи: "))
                manager.start_task(task_id)
                print("Таймер успешно запущен.")

            elif choice == "4":
                task_id = int(input("Введите ID задачи: "))
                elapsed = manager.stop_task(task_id)

                print(
                    "Таймер остановлен. Время сессии: "
                    + manager.timer.format_time(elapsed)
                )

            elif choice == "5":
                task_id = int(input("Введите ID задачи: "))
                seconds = manager.get_task_time(task_id)

                print(
                    "Общее затраченное время: "
                    + manager.timer.format_time(seconds)
                )

            elif choice == "6":
                task_id = int(input("Введите ID задачи: "))

                print("Доступные статусы:")
                print("1. To Do")
                print("2. In Progress")
                print("3. Done")

                status_choice = input("Выберите статус: ")

                statuses = {
                    "1": "To Do",
                    "2": "In Progress",
                    "3": "Done"
                }

                if status_choice not in statuses:
                    print("Некорректный выбор статуса.")
                    continue

                status = statuses[status_choice]

                if status == "Done":
                    manager.complete_task(task_id)
                else:
                    if manager.timer.is_running(task_id):
                        raise ValueError(
                            "Сначала остановите таймер задачи"
                        )
                    manager.update_status(task_id, status)

                print("Статус задачи успешно изменён.")

            elif choice == "7":
                task_id = int(input("Введите ID задачи: "))
                manager.complete_task(task_id)
                print("Задача успешно завершена.")

            elif choice == "8":
                print("\n" + reports.generate_report())

            elif choice == "9":
                filename = reports.save_report()
                print(f"Отчёт сохранён в файл: {filename}")

            elif choice == "0":
                print("Работа программы завершена.")
                break

            else:
                print("Неверный пункт меню. Повторите ввод.")

        except (ValueError, OSError) as error:
            print(f"Ошибка: {error}")

        except (KeyboardInterrupt, EOFError):
            print("\nРабота программы прервана.")
            break


if __name__ == "__main__":
    main()
