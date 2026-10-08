"""
Генератор учебных материалов EduForge.

Загружает базовый системный промпт, формирует запрос
с учётом темы и языка и передаёт его выбранной AI-модели.
"""

from pathlib import Path

from models import ModelFactory


PROMPT_PATH = Path("prompts/base_prompt.txt")


class MethodologyGenerator:
    """Создаёт учебные методички с помощью выбранной AI-модели."""

    def __init__(self, provider: str, api_key: str):
        self.provider = provider
        self.api_key = api_key
        self.system_prompt = self._load_prompt()

    def _load_prompt(self) -> str:
        """Загружает базовый системный промпт из файла."""

        if not PROMPT_PATH.exists():
            raise FileNotFoundError(
                f"Файл промпта не найден: {PROMPT_PATH}"
            )

        return PROMPT_PATH.read_text(encoding="utf-8")

    def generate(self, topic: str, language: str) -> str:
        """Генерирует методичку по указанной теме и языку."""

        if not topic.strip():
            raise ValueError("Тема методички не может быть пустой.")

        user_prompt = (
            f"Язык методички: {language}\n\n"
            f"Тема методички: {topic.strip()}"
        )

        model = ModelFactory.create(
            provider=self.provider,
            api_key=self.api_key,
            system_prompt=self.system_prompt,
        )

        return model.ask(user_prompt)