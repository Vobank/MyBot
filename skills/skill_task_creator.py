NAME = "task_creator"
DESCRIPTION = "Создает, изменяет и удаляет задачи в системе задач Windows."
PARAMS = {
    "action": "действие (create, update, delete)",
    "task_name": "имя задачи",
    "trigger": "триггер (time, event, logon, startup)",
    "command": "команда для выполнения (для создания и обновления)",
    "start_time": "время начала (для триггера time, формат HH:MM)",
    "interval": "интервал в минутах (для триггера time, опционально)"
}
DANGEROUS = True

def run(action="create", task_name="", trigger="", command="", start_time="", interval=""):
    import subprocess
    import re

    if not task_name:
        return "Укажите имя задачи."
    if not action:
        return "Укажите действие (create, update, delete)."
    
    if action == "create":
        if not trigger or not command:
            return "Для создания задачи укажите триггер и команду."
        if trigger == "time":
            if not start_time:
                return "Для триггера time укажите время начала."
            task_command = f'schtasks /create /tn "{task_name}" /tr "{command}" /sc minute /mo {interval if interval else "60"} /st {start_time}'
        elif trigger == "logon":
            task_command = f'schtasks /create /tn "{task_name}" /tr "{command}" /sc onlogon'
        elif trigger == "startup":
            task_command = f'schtasks /create /tn "{task_name}" /tr "{command}" /sc onstart'
        else:
            return "Триггер не поддерживается."
    elif action == "update":
        if not command:
            return "Для обновления задачи укажите новую команду."
        task_command = f'schtasks /change /tn "{task_name}" /tr "{command}"'
    elif action == "delete":
        task_command = f'schtasks /delete /tn "{task_name}" /f'
    else:
        return "Действие не поддерживается."
    
    try:
        result = subprocess.run(task_command, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            return f"Ошибка при выполнении: {result.stderr}"
        return result.stdout
    except Exception as e:
        return f"Произошла ошибка: {e}"