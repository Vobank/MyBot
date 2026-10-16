import os
import subprocess

NAME = "manage_venv_versions"
DESCRIPTION = "Создание и удаление виртуальных окружений Python с указанием версии Python."

def run(text=""):
    commands = text.split()
    if len(commands) < 3:
        return "Неверный формат команды. Пример использования: 'create venv_name python3.9' или 'delete venv_name'"
    
    action, venv_name, python_version = commands[0], commands[1], commands[2]
    
    venv_path = os.path.join(os.getcwd(), venv_name)
    
    if action == 'create':
        try:
            subprocess.run([python_version, '-m', 'venv', venv_path], check=True)
            return f"Виртуальное окружение {venv_name} успешно создано с версией Python {python_version}."
        except subprocess.CalledProcessError as e:
            return f"Ошибка при создании виртуального окружения: {e}"
    elif action == 'delete':
        try:
            subprocess.run(['rm', '-rf', venv_path], check=True)
            return f"Виртуальное окружение {venv_name} успешно удалено."
        except subprocess.CalledProcessError as e:
            return f"Ошибка при удалении виртуального окружения: {e}"
    else:
        return "Неверная команда. Используйте 'create' или 'delete'."