"""
Тест подключения к Gemini API.

Проверяет API-ключ, установленный через .env,
и выполняет минимальный запрос к Gemini без участия CodeMentor.
"""

import os

from dotenv import load_dotenv
from google import genai


def main():
    """Проверяет доступность Gemini API."""

    load_dotenv()

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        print("ОШИБКА: GEMINI_API_KEY не найден.")
        return

    print("API-ключ найден.")
    print("Создаём Gemini client...")

    client = genai.Client(api_key=api_key)

    print("Отправляем тестовый запрос...")

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents="Ответь одним предложением: работает ли Gemini API?",
    )

    print("\nОтвет Gemini:")
    print("=" * 60)
    print(response.text)
    print("=" * 60)


if __name__ == "__main__":
    main()