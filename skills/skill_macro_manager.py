import os
import json
import subprocess

NAME = "macro_manager"
DESCRIPTION = "Создание и управление макросами для автоматизации действий на ПК"

MACROS_PATH = os.path.expanduser("~/.mybot/macros.json")

def load_macros():
    if not os.path.exists(MACROS_PATH):
        return {}
    with open(MACROS_PATH, "r") as f:
        return json.load(f)

def save_macros(macros):
    os.makedirs(os.path.dirname(MACROS_PATH), exist_ok=True)
    with open(MACROS_PATH, "w") as f:
        json.dump(macros, f, indent=4)

def run(text=""):
    if not text:
        return "Пожалуйста, укажите действие: создать, запустить или удалить макрос."

    command, *params = text.split()
    
    macros = load_macros()

    if command == "создать":
        name, steps = params[0], params[1:]
        macros[name] = steps
        save_macros(macros)
        return f"Макрос '{name}' создан."
    
    elif command == "запустить":
        name = params[0]
        if name not in macros:
            return f"Макрос '{name}' не найден."
        for step in macros[name]:
            subprocess.run(step.split())
        return f"Макрос '{name}' запущен."
    
    elif command == "удалить":
        name = params[0]
        if name not in macros:
            return f"Макрос '{name}' не найден."
        del macros[name]
        save_macros(macros)
        return f"Макрос '{name}' удален."
    
    else:
        return "Неизвестная команда. Используйте создать, запустить или удалить."