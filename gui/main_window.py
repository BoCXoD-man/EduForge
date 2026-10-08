"""
Главное окно графического интерфейса EduForge.

Окно позволяет выбрать AI-модель, язык и формат,
ввести тему и запустить генерацию учебной методички.
"""

from PySide6.QtCore import QThread
from PySide6.QtWidgets import (
    QComboBox,
    QFormLayout,
    QGroupBox,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from gui.worker import GenerationWorker
from tools.file_tools import save_markdown


class MainWindow(QMainWindow):
    """Главное окно приложения EduForge."""

    def __init__(self, api_keys: dict[str, str | None]):
        super().__init__()

        self.api_keys = api_keys

        self.thread = None
        self.worker = None

        self.setWindowTitle("EduForge")
        self.setMinimumSize(600, 450)

        self._create_widgets()
        self._create_layout()
        self._connect_signals()

    def _create_widgets(self):
        """Создаёт элементы интерфейса."""

        self.model_combo = QComboBox()
        self.model_combo.addItem("OpenRouter", "openrouter")
        self.model_combo.addItem("Gemini", "gemini")
        self.model_combo.addItem("ChatGPT (OpenAI)", "openai")

        self.language_combo = QComboBox()
        self.language_combo.addItems(["Русский","English",])

        self.format_combo = QComboBox()
        self.format_combo.addItem("Markdown (.md)","md",)
        self.format_combo.addItem("PDF (.pdf)","pdf",)
        self.format_combo.setCurrentIndex(0)

        self.topic_input = QLineEdit()
        self.topic_input.setPlaceholderText(
            "Например: Циклы for и while в Python"
        )

        self.generate_button = QPushButton("Создать методичку")

        self.status_label = QLabel("Готов к работе.")

    def _create_layout(self):
        """Создаёт и настраивает компоновку элементов интерфейса."""

        settings_group = QGroupBox("Параметры методички")
        settings_layout = QFormLayout()

        settings_layout.addRow("AI-модель:", self.model_combo)
        settings_layout.addRow("Язык:", self.language_combo)
        settings_layout.addRow("Формат:", self.format_combo)
        settings_layout.addRow("Тема:", self.topic_input)

        settings_group.setLayout(settings_layout)

        main_layout = QVBoxLayout()
        main_layout.addWidget(settings_group)
        main_layout.addWidget(self.generate_button)
        main_layout.addWidget(self.status_label)
        main_layout.addStretch()

        central_widget = QWidget()
        central_widget.setLayout(main_layout)

        self.setCentralWidget(central_widget)

    def _connect_signals(self):
        """Подключает обработчики событий интерфейса."""

        self.generate_button.clicked.connect(
            self._on_generate_clicked
        )

    def _on_generate_clicked(self):
        """Проверяет параметры и запускает генерацию."""

        topic = self.topic_input.text().strip()

        if not topic:
            self.status_label.setText("Введите тему методички.")
            return

        file_format = self.format_combo.currentData()

        if file_format == "pdf":
            self.status_label.setText(
                "Генерация PDF пока не реализована."
            )
            return

        provider = self.model_combo.currentData()
        language = self.language_combo.currentText()
        api_key = self.api_keys.get(provider)

        if not api_key:
            self.status_label.setText(
                "Для выбранной модели не найден API-ключ."
            )
            return

        self.generate_button.setEnabled(False)
        self.status_label.setText(
            "Генерация методички... Пожалуйста, подождите."
        )

        self.thread = QThread()
        self.worker = GenerationWorker(
            provider=provider,
            api_key=api_key,
            topic=topic,
            language=language,
        )

        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)

        self.worker.finished.connect(self._on_generation_finished)
        self.worker.error.connect(self._on_generation_error)

        self.worker.finished.connect(self.thread.quit)
        self.worker.error.connect(self.thread.quit)

        self.thread.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.finished.connect(self._on_thread_finished)

        self.thread.start()

    def _on_generation_finished(self, content: str):
        """Сохраняет успешно сгенерированную методичку."""

        topic = self.topic_input.text().strip()

        try:
            file_path = save_markdown(
                title=topic,
                content=content,
            )

        except Exception as exc:
            self._on_generation_error(
                f"Не удалось сохранить файл: {exc}"
            )
            return

        self.status_label.setText(
            f"Методичка сохранена: {file_path}"
        )

        QMessageBox.information(
            self,
            "Готово",
            f"Методичка успешно создана.\n\n"
            f"Файл:\n{file_path}",
        )

    def _on_generation_error(self, message: str):
        """Показывает пользователю ошибку генерации."""

        self.status_label.setText(
            f"Ошибка: {message}"
        )

        QMessageBox.critical(
            self,
            "Ошибка",
            message,
        )

    def _on_thread_finished(self):
        """Освобождает ссылки на завершившийся поток."""

        self.generate_button.setEnabled(True)

        self.thread = None
        self.worker = None