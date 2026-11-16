
import unittest
from unittest.mock import patch
from io import StringIO

from main import main


class TestMain(unittest.TestCase):
    """Тестирование главного меню программы."""

    @patch("builtins.input", return_value="0")
    @patch("sys.stdout", new_callable=StringIO)
    def test_exit(self, mock_stdout, mock_input):
        """Проверка корректного завершения программы."""
        main()

        output = mock_stdout.getvalue()

        self.assertIn(
            "Работа программы завершена",
            output
        )

    @patch("builtins.input", side_effect=["99", "0"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_invalid_choice(self, mock_stdout, mock_input):
        """Проверка обработки неверного пункта меню."""
        main()

        output = mock_stdout.getvalue()

        self.assertIn(
            "Неверный пункт меню",
            output
        )

    @patch(
        "builtins.input",
        side_effect=["1", "Тестовая задача", "Описание", "2", "0"]
    )
    @patch("sys.stdout", new_callable=StringIO)
    def test_create_and_view_task(self, mock_stdout, mock_input):
        """Проверка создания и просмотра задачи."""
        main()

        output = mock_stdout.getvalue()

        self.assertIn("Задача создана! ID: 1", output)
        self.assertIn("Тестовая задача", output)
        self.assertIn("To Do", output)

    @patch("builtins.input", side_effect=["8", "0"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_generate_empty_report(self, mock_stdout, mock_input):
        """Проверка формирования отчёта через меню."""
        main()

        output = mock_stdout.getvalue()

        self.assertIn("ОТЧЁТ ПО УЧЁТУ ВРЕМЕНИ", output)
        self.assertIn("Всего задач: 0", output)


if __name__ == "__main__":
    unittest.main()
