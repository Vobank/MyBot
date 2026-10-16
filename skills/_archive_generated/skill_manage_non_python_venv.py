NAME = "manage_non_python_venv"
DESCRIPTION = "Создание и управление виртуальными окружениями для проектов на других языках программирования."

import os
import subprocess

def run(text=""):
    commands = text.split()
    if len(commands) < 2:
        return "Недостаточно параметров. Используйте: manage_non_python_venv <action> [params]"

    action = commands[1]

    if action == "create":
        if len(commands) < 3:
            return "Недостаточно параметров. Используйте: manage_non_python_venv create <language>"
        language = commands[2]
        venv_path = os.path.join(os.getcwd(), f"{language}_venv")
        if language == "node":
            result = subprocess.run(["npm", "install", "-g", "nvm"], capture_output=True, text=True)
            if result.returncode != 0:
                return f"Ошибка установки nvm: {result.stderr}"
            result = subprocess.run(["nvm", "install", "node"], capture_output=True, text=True)
            if result.returncode != 0:
                return f"Ошибка установки node.js: {result.stderr}"
            result = subprocess.run(["nvm", "use", "node"], capture_output=True, text=True)
            if result.returncode != 0:
                return f"Ошибка использования node.js: {result.stderr}"
            result = subprocess.run(["npm", "install", "-g", "yarn"], capture_output=True, text=True)
            if result.returncode != 0:
                return f"Ошибка установки yarn: {result.stderr}"
            result = subprocess.run(["yarn", "global", "add", "create-react-app"], capture_output=True, text=True)
            if result.returncode != 0:
                return f"Ошибка установки create-react-app: {result.stderr}"
            return "Виртуальное окружение для node.js создано."
        elif language == "ruby":
            result = subprocess.run(["gem", "install", "bundler"], capture_output=True, text=True)
            if result.returncode != 0:
                return f"Ошибка установки bundler: {result.stderr}"
            return "Виртуальное окружение для ruby создано."
        else:
            return f"Язык программирования {language} не поддерживается."

    elif action == "delete":
        if len(commands) < 3:
            return "Недостаточно параметров. Используйте: manage_non_python_venv delete <language>"
        language = commands[2]
        venv_path = os.path.join(os.getcwd(), f"{language}_venv")
        if os.path.exists(venv_path):
            try:
                os.rmdir(venv_path)
                return f"Виртуальное окружение для {language} удалено."
            except Exception as e:
                return f"Ошибка при удалении виртуального окружения для {language}: {str(e)}"
        else:
            return f"Виртуальное окружение для {language} не существует."

    else:
        return f"Действие {action} не поддерживается."

    return "Успешно выполнено."