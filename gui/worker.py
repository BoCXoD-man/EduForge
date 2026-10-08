"""
Рабочий поток генерации методички EduForge.

Worker выполняет обращение к AI-модели вне основного GUI-потока,
чтобы интерфейс приложения оставался отзывчивым во время генерации.
"""

from PySide6.QtCore import QObject, Signal, Slot

from generator import MethodologyGenerator


class GenerationWorker(QObject):
    """Выполняет генерацию методички в отдельном потоке."""

    finished = Signal(str)
    error = Signal(str)

    def __init__(
        self,
        provider: str,
        api_key: str,
        topic: str,
        language: str,
    ):
        super().__init__()

        self.provider = provider
        self.api_key = api_key
        self.topic = topic
        self.language = language

    @Slot()
    def run(self):
        """Запускает генерацию методички и передаёт результат."""

        try:
            generator = MethodologyGenerator(
                provider=self.provider,
                api_key=self.api_key,
            )

            result = generator.generate(
                topic=self.topic,
                language=self.language,
            )

            self.finished.emit(result)

        except Exception as exc:
            self.error.emit(str(exc))