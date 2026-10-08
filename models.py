"""
AI-модели для EduForge.

Файл содержит общий интерфейс AI-модели и реализации
для OpenAI, Gemini и OpenRouter.
"""

from abc import ABC, abstractmethod

from google import genai
from google.genai import types
from openai import OpenAI


class BaseModel(ABC):
    """Базовый интерфейс AI-моделей EduForge."""

    def __init__(self, system_prompt: str):
        self.system_prompt = system_prompt

    @abstractmethod
    def ask(self, user_prompt: str) -> str:
        """Отправляет запрос модели и возвращает текстовый ответ."""
        raise NotImplementedError


class OpenAIModel(BaseModel):
    """Модель OpenAI для генерации учебных материалов."""

    def __init__(self, api_key: str, system_prompt: str):
        super().__init__(system_prompt)

        self.client = OpenAI(api_key=api_key)

    def ask(self, user_prompt: str) -> str:
        """Отправляет запрос в OpenAI и возвращает ответ."""

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": self.system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
        )

        return response.choices[0].message.content.strip()


class GeminiModel(BaseModel):
    """Модель Gemini для генерации учебных материалов."""

    def __init__(self, api_key: str, system_prompt: str):
        super().__init__(system_prompt)

        self.client = genai.Client(api_key=api_key)

    def ask(self, user_prompt: str) -> str:
        """Отправляет запрос в Gemini и возвращает ответ."""

        response = self.client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=user_prompt,
            config=types.GenerateContentConfig(
                system_instruction=self.system_prompt,
            ),
        )

        return response.text.strip()


class OpenRouterModel(BaseModel):
    """Модель OpenRouter для генерации учебных материалов."""

    def __init__(self, api_key: str, system_prompt: str):
        super().__init__(system_prompt)

        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )

    def ask(self, user_prompt: str) -> str:
        """Отправляет запрос в OpenRouter и возвращает ответ."""

        response = self.client.chat.completions.create(
            model="openrouter/free",
            messages=[
                {
                    "role": "system",
                    "content": self.system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
        )

        return response.choices[0].message.content.strip()


class ModelFactory:
    """Создаёт AI-модель на основе выбранного провайдера."""

    @staticmethod
    def create(
        provider: str,
        api_key: str,
        system_prompt: str,
    ) -> BaseModel:
        """Возвращает реализацию модели для указанного провайдера."""

        models = {
            "openai": OpenAIModel,
            "gemini": GeminiModel,
            "openrouter": OpenRouterModel,
        }

        model_class = models.get(provider)

        if model_class is None:
            raise ValueError(
                f"Неподдерживаемый AI-провайдер: {provider}"
            )

        return model_class(
            api_key=api_key,
            system_prompt=system_prompt,
        )