import os
import subprocess

NAME = "advanced_venv_management"
DESCRIPTION = "Создает, удаляет и управляют виртуальными окружениями Python с дополнительными параметрами."

def run(text=""):
    args = text.split()
    if not args:
        return "Пожалуйста, укажите действие (create/delete/list) и имя виртуального окружения."
    
    action = args[0]
    venv_name = args[1] if len(args) > 1 else ""
    
    if action == "create":
        if venv_name:
            subprocess.run(["python", "-m", "venv", venv_name])
            return f"Виртуальное окружение {venv_name} создано."
        else:
            return "Пожалуйста, укажите имя виртуального окружения."
    elif action == "delete":
        if venv_name:
            subprocess.run(["rm", "-rf", venv_name])
            return f"Виртуальное окружение {venv_name} удалено."
        else:
            return "Пожалуйста, укажите имя виртуального окружения."
    elif action == "list":
        venvs = [d for d in os.listdir() if os.path.isdir(d) and os.path.exists(os.path.join(d, "bin", "activate"))]
        return "Список виртуальных окружений: " + ", ".join(venvs) if venvs else "Нет созданных виртуальных окружений."
    else:
        return "Неподдерживаемое действие. Используйте create, delete или list."