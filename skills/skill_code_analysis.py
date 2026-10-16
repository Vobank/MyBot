import subprocess
import os

NAME = "code_analysis"
DESCRIPTION = "Анализирует код на наличие ошибок и предлагает исправления."

def run(file_path=""):
    if not os.path.isfile(file_path):
        return "Файл не найден."

    try:
        # Используем flake8 для анализа кода
        result = subprocess.run(['flake8', file_path], capture_output=True, text=True)
        errors = result.stdout

        if errors:
            return f"Найдены ошибки:\n{errors}"
        else:
            return "Ошибок не найдено."
    except Exception as e:
        return f"Произошла ошибка: {str(e)}"