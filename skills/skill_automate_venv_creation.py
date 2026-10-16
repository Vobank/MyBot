import os
import subprocess

NAME = "automate_venv_creation"
DESCRIPTION = "Создает виртуальное окружение Python с автоматическим выбором версии Python"

def run(text=""):
    python_versions = ["python3", "python3.9", "python3.8", "python3.7"]
    venv_path = text.strip() or "new_venv"
    
    for version in python_versions:
        try:
            subprocess.run([version, "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            subprocess.run([version, "-m", "venv", venv_path], check=True)
            return f"Виртуальное окружение создано с помощью {version} в {venv_path}"
        except subprocess.CalledProcessError:
            continue
    
    return "Не удалось найти подходящую версию Python для создания виртуального окружения"