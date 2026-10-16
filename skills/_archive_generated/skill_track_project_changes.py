import os
from datetime import datetime

NAME = "track_project_changes"
DESCRIPTION = "Отслеживает изменения в проекте и уведомляет об изменениях файлов"

def run(directory="."):
    try:
        # Получаем список файлов в директории
        files = os.listdir(directory)
        changes = []

        # Запоминаем текущее состояние файлов
        file_states = {f: os.path.getmtime(os.path.join(directory, f)) for f in files}

        # Функция для проверки изменений
        def check_changes():
            new_states = {f: os.path.getmtime(os.path.join(directory, f)) for f in os.listdir(directory)}
            for file, old_time in file_states.items():
                new_time = new_states.get(file)
                if new_time and new_time > old_time:
                    changes.append(f"Изменения в файле: {file} в {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        # Запускаем проверку изменений
        check_changes()
        
        # Возвращаем уведомления о изменениях
        return "\n".join(changes) if changes else "Нет изменений в проекте"

    except Exception as e:
        return f"Ошибка при отслеживании изменений: {str(e)}"