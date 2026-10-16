import os
import subprocess

NAME = "show_installed_packages"
DESCRIPTION = "Показывает список установленных пакетов в виртуальном окружении"

def run(text=""):
    venv_path = os.environ.get('VIRTUAL_ENV')
    if not venv_path:
        return "Виртуальное окружение не активировано."
    
    try:
        result = subprocess.run([os.path.join(venv_path, 'bin', 'pip'), 'list'], capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Произошла ошибка: {e.stderr}"