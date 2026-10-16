import subprocess
import os

NAME = "schedule_task"
DESCRIPTION = "Создает и управляет задачами по расписанию."

def run(text=""):
    command_parts = text.split()
    
    if not command_parts:
        return "Пожалуйста, укажите действие (create/delete/list) и команду или имя задачи."
    
    action = command_parts[0].lower()
    
    if action == "create":
        if len(command_parts) < 3:
            return "Пожалуйста, укажите время (cron-синтаксис) и команду для задачи."
        
        schedule_time = command_parts[1]
        command_to_run = " ".join(command_parts[2:])
        task_name = f"task_{command_to_run.replace(' ', '_')}"
        
        # Создание задачи по расписанию (пример для Unix-like систем)
        cron_command = f"(crontab -l ; echo '{schedule_time} /usr/bin/python3 -c \"import os; os.system(\\\"{command_to_run}\\\")\"') | crontab -"
        try:
            subprocess.run(cron_command, shell=True, check=True)
            return f"Задача '{task_name}' успешно создана по расписанию."
        except subprocess.CalledProcessError as e:
            return f"Ошибка при создании задачи: {e}"
    
    elif action == "delete":
        if len(command_parts) < 2:
            return "Пожалуйста, укажите имя задачи для удаления."
        
        task_name = " ".join(command_parts[1:])
        try:
            subprocess.run(f"crontab -l | grep -v '{task_name}' | crontab -", shell=True, check=True)
            return f"Задача '{task_name}' успешно удалена."
        except subprocess.CalledProcessError as e:
            return f"Ошибка при удалении задачи: {e}"
    
    elif action == "list":
        try:
            output = subprocess.check_output("crontab -l", shell=True).decode()
            return f"Список задач по расписанию:\n{output}"
        except subprocess.CalledProcessError as e:
            return f"Ошибка при получении списка задач: {e}"
    
    else:
        return "Неизвестное действие. Доступные действия: create, delete, list."