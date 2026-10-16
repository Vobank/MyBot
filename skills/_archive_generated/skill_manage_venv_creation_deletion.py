import os
import subprocess

NAME = "manage_venv_creation_deletion"
DESCRIPTION = "Создание и удаление виртуальных окружений Python"

def run(text=""):
    command = text.lower().strip()
    parts = command.split()
    
    if len(parts) < 2:
        return "Необходимо указать действие (создать/удалить) и имя виртуального окружения."

    action = parts[0]
    venv_name = parts[1]

    if action == "создать":
        try:
            subprocess.run([sys.executable, "-m", "venv", venv_name], check=True)
            return f"Виртуальное окружение {venv_name} успешно создано."
        except subprocess.CalledProcessError as e:
            return f"Ошибка при создании виртуального окружения: {e}"
    elif action == "удалить":
        if os.path.exists(venv_name):
            try:
                subprocess.run(["rm", "-r", venv_name], check=True)
                return f"Виртуальное окружение {venv_name} успешно удалено."
            except subprocess.CalledProcessError as e:
                return f"Ошибка при удалении виртуального окружения: {e}"
        else:
            return f"Виртуальное окружение {venv_name} не существует."
    else:
        return "Неизвестное действие. Используйте 'создать' или 'удалить'."