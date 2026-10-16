import os
import subprocess

NAME = "auto_venv_requirements"
DESCRIPTION = "Автоматически создавать и управлять виртуальными окружениями для проектов на основе файлов requirements.txt"

def run(text=""):
    project_path = text.strip()
    
    if not os.path.exists(project_path):
        return "Проект по указанному пути не существует."
    
    requirements_path = os.path.join(project_path, "requirements.txt")
    if not os.path.exists(requirements_path):
        return "Файл requirements.txt не найден в проекте."
    
    venv_path = os.path.join(project_path, "venv")
    if not os.path.exists(venv_path):
        subprocess.run(["python", "-m", "venv", venv_path], check=True)
        print(f"Создано виртуальное окружение: {venv_path}")
    
    activate_script = os.path.join(venv_path, "Scripts", "activate") if os.name == "nt" else os.path.join(venv_path, "bin", "activate")
    
    pip_install_cmd = f"source {activate_script} && pip install -r {requirements_path}" if os.name != "nt" else f"{activate_script} && pip install -r {requirements_path}"
    
    result = subprocess.run(pip_install_cmd, shell=True, check=True, capture_output=True, text=True)
    
    return f"Установлены пакеты из requirements.txt:\n{result.stdout}"