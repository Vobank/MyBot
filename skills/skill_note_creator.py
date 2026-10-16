import os
import re

NAME = "note_creator"
DESCRIPTION = "Создает заметки на основе контекста и ключевых слов из открытых файлов"

def run(text=""):
    # Пример: Ищем ключевые слова и создаем заметку
    keywords = ["important", "note", "todo", "fix"]
    notes_directory = "C:\\Users\\User\\Notes"
    if not os.path.exists(notes_directory):
        os.makedirs(notes_directory)

    # Предполагаем, что мы знаем список открытых файлов (например, из активных окон)
    open_files = ["C:\\Users\\User\\Documents\\project\\file1.py", "C:\\Users\\User\\Documents\\project\\file2.py"]
    for file_path in open_files:
        with open(file_path, 'r') as file:
            content = file.read()
            for keyword in keywords:
                matches = re.findall(f'(?i)\b{keyword}\b.*', content)
                for match in matches:
                    note_filename = os.path.join(notes_directory, f"{os.path.basename(file_path)}_{keyword}.txt")
                    with open(note_filename, 'a') as note_file:
                        note_file.write(f"From {file_path}: {match}\n")

    return "Заметки созданы на основе ключевых слов из открытых файлов"