"""
Инструменты для сохранения результатов CodeMentor.

Файл отвечает за создание выходной директории и безопасное
сохранение сгенерированных учебных материалов в Markdown.
"""

import re
from pathlib import Path


DEFAULT_OUTPUT_DIR = Path("output")


def sanitize_filename(filename: str) -> str:
    """Удаляет недопустимые для имени файла символы."""

    filename = filename.strip()

    if not filename:
        return "methodology"

    filename = re.sub(r'[<>:"/\\|?*]', "_", filename)
    filename = re.sub(r"\s+", "_", filename)

    return filename


def save_markdown(
    title: str,
    content: str,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
) -> Path:
    """Сохраняет методичку в Markdown-файл и возвращает путь к нему."""

    output_dir.mkdir(parents=True, exist_ok=True)

    filename = f"{sanitize_filename(title)}.md"
    file_path = output_dir / filename

    file_path.write_text(content, encoding="utf-8")

    return file_path