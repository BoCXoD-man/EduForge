"""
Инструменты для сохранения результатов EduForge.

Файл отвечает за создание выходной директории и сохранение
сгенерированных учебных материалов в Markdown и PDF.
"""

import re
from pathlib import Path

import markdown
from PySide6.QtGui import QTextDocument
from PySide6.QtPrintSupport import QPrinter


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


def save_pdf(
    title: str,
    content: str,
    output_dir: Path = DEFAULT_OUTPUT_DIR) -> Path:
    """Преобразует Markdown в HTML и сохраняет результат в PDF."""

    output_dir.mkdir(parents=True, exist_ok=True)

    filename = f"{sanitize_filename(title)}.pdf"
    file_path = output_dir / filename

    html_content = markdown.markdown(
        content,
        extensions=["fenced_code", "tables"],
    )

    html = f"""
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{
                font-family: Arial, sans-serif;
                font-size: 11pt;
                line-height: 1.5;
            }}

            h1 {{
                font-size: 24pt;
                margin-bottom: 18pt;
            }}

            h2 {{
                font-size: 18pt;
                margin-top: 18pt;
                margin-bottom: 10pt;
            }}

            h3 {{
                font-size: 14pt;
                margin-top: 14pt;
                margin-bottom: 8pt;
            }}

            p {{
                margin: 0 0 10pt 0;
            }}

            pre {{
                font-family: Consolas, monospace;
                font-size: 9pt;
                background-color: #f2f2f2;
                padding: 8pt;
            }}

            code {{
                font-family: Consolas, monospace;
            }}

            table {{
                border-collapse: collapse;
                width: 100%;
            }}

            th, td {{
                border: 1px solid #999;
                padding: 5pt;
            }}

            th {{
                font-weight: bold;
            }}
        </style>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """

    document = QTextDocument()
    document.setHtml(html)

    printer = QPrinter(QPrinter.HighResolution)
    printer.setOutputFormat(QPrinter.PdfFormat)
    printer.setOutputFileName(str(file_path))

    document.print_(printer)

    return file_path
