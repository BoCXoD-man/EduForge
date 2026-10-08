"""
Точка входа в приложение EduForge.

Загружает переменные окружения, создаёт Qt-приложение
и запускает главное окно.
"""

import os
import sys

from dotenv import load_dotenv
from PySide6.QtWidgets import QApplication

from gui.main_window import MainWindow


def main():
    """Запускает графический интерфейс EduForge."""

    load_dotenv()

    app = QApplication(sys.argv)

    window = MainWindow(
        api_keys={
            "openai": os.getenv("OPENAI_API_KEY"),
            "gemini": os.getenv("GEMINI_API_KEY"),
            "openrouter": os.getenv("OPENROUTER_API_KEY"),
        }
    )

    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()