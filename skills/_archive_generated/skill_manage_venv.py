NAME = "manage_venv"
DESCRIPTION = "Создает, активирует и удаляет виртуальные окружения Python."
PARAMS = {"action": "действие (create, activate, delete)", "venv_name": "имя виртуального окружения"}
DANGEROUS = True  # Удаление виртуального окружения может быть опасным

def run(action="create", venv_name="my_venv"):
    import os
    import subprocess

    try:
        if action == "create":
            if not venv_name:
                return "Укажи имя виртуального окружения."
            subprocess.run(["python", "-m", "venv", venv_name], check=True)
            return f"Виртуальное окружение {venv_name} создано."

        elif action == "activate":
            if not venv_name:
                return "Укажи имя виртуального окружения."
            if os.name == "nt":  # Windows
                activate_path = os.path.join(venv_name, "Scripts", "activate")
            else:  # Unix-based systems
                activate_path = os.path.join(venv_name, "bin", "activate")
            if not os.path.exists(activate_path):
                return f"Виртуальное окружение {venv_name} не существует."
            return f"Для активации используй команду: source {activate_path}"

        elif action == "delete":
            if not venv_name:
                return "Укажи имя виртуального окружения."
            venv_path = venv_name
            if os.path.exists(venv_path):
                subprocess.run(["rm", "-rf", venv_path], check=True)
                return f"Виртуальное окружение {venv_name} удалено."
            else:
                return f"Виртуальное окружение {venv_name} не существует."

        else:
            return "Неверное действие. Используй create, activate или delete."
    except Exception as e:
        return f"Ошибка: {e}"

    return "Неизвестная ошибка."