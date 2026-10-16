import os
import subprocess

NAME = "hotkey_manager"
DESCRIPTION = "Создание и управление простыми горячими клавишами"

def run(text=""):
    command = text.strip().split()
    if len(command) < 3:
        return "Неверный формат команды. Используйте: 'hotkey [action] [key_combination] [command]'"
    
    action = command[0]
    key_combination = command[1]
    command_to_run = ' '.join(command[2:])

    if action == "add":
        hotkey_file = os.path.expanduser(f"~/.hotkeys/{key_combination}.sh")
        os.makedirs(os.path.dirname(hotkey_file), exist_ok=True)
        with open(hotkey_file, 'w') as file:
            file.write(f"#!/bin/bash\n{command_to_run}")
        subprocess.run(["chmod", "+x", hotkey_file])
        return f"Горячая клавиша '{key_combination}' добавлена для выполнения команды '{command_to_run}'"
    elif action == "remove":
        hotkey_file = os.path.expanduser(f"~/.hotkeys/{key_combination}.sh")
        if os.path.exists(hotkey_file):
            os.remove(hotkey_file)
            return f"Горячая клавиша '{key_combination}' удалена"
        else:
            return f"Горячая клавиша '{key_combination}' не найдена"
    else:
        return "Неверное действие. Используйте 'add' или 'remove'"