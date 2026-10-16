import os
import re

NAME = "find_strings"
DESCRIPTION = "Находит строки в файлах по заданному шаблону"

def run(pattern=""):
    results = []
    # Пробегаемся по всем файлам в текущей директории
    for root, dirs, files in os.walk("."):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    # Ищем строки по шаблону
                    for line_number, line in enumerate(lines, 1):
                        if re.search(pattern, line):
                            results.append(f"{file_path}:{line_number}:{line.strip()}")
            except Exception as e:
                pass  # Пропускаем файлы, которые не удалось открыть
    return "\n".join(results) if results else "Ничего не найдено"