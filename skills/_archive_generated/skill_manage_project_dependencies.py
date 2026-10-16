import os
import subprocess

NAME = "manage_project_dependencies"
DESCRIPTION = "Автоматически создает и управляется списком зависимостей проекта"

def run(text=""):
    project_path = text.strip() if text.strip() else os.getcwd()
    requirements_file = os.path.join(project_path, "requirements.txt")

    try:
        # Создаем или обновляем файл requirements.txt
        subprocess.run(["pip", "freeze", ">", "requirements.txt"], cwd=project_path, shell=True, check=True)
        return f"Список зависимостей проекта успешно создан/обновлен в файле {requirements_file}"
    except subprocess.CalledProcessError as e:
        return f"Произошла ошибка при создании/обновлении списка зависимостей: {e}"