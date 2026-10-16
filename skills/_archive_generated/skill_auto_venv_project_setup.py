import os
import subprocess
import json

NAME = "auto_venv_project_setup"
DESCRIPTION = "Автоматически создает и настраивает виртуальное окружение для проекта на основе файла requirements.txt"

def run(text=""):
    project_path = text.strip()
    
    if not os.path.isdir(project_path):
        return f"Проект по пути {project_path} не найден."
    
    requirements_path = os.path.join(project_path, "requirements.txt")
    if not os.path.isfile(requirements_path):
        return f"Файл requirements.txt не найден в проекте {project_path}."
    
    venv_path = os.path.join(project_path, "venv")
    if not os.path.isdir(venv_path):
        subprocess.run(["python", "-m", "venv", venv_path], check=True)
    
    activate_script = "source venv/bin/activate" if os.name == "posix" else "venv\\Scripts\\activate"
    pip_command = f"{activate_script} && pip install -r {requirements_path}"
    subprocess.run(["bash", "-c", pip_command] if os.name == "posix" else ["cmd", "/c", pip_command], cwd=project_path, check=True)
    
    return f"Виртуальное окружение для проекта {project_path} успешно создано и настроено."