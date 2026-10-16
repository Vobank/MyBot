NAME = "task_scheduler_manager"
DESCRIPTION = "Управляет задачами в планировщике задач Windows: добавляет, удаляет и изменяет задачи."
PARAMS = {
    "action": "действие (add, delete, modify)",
    "task_name": "имя задачи",
    "trigger": "триггер задачи (e.g., Daily, AtStartup)",
    "start_time": "время начала задачи (для триггера Daily, формат HH:MM)",
    "program": "путь к программе, которую нужно запустить",
    "arguments": "аргументы для запуска программы",
    "description": "описание задачи"
}
DANGEROUS = True

def run(action="add", task_name="", trigger="", start_time="", program="", arguments="", description=""):
    import os
    import subprocess

    if not task_name:
        return "Укажите имя задачи."

    actions = ["add", "delete", "modify"]
    if action not in actions:
        return f"Действие {action} не поддерживается. Используйте: {', '.join(actions)}."

    if action == "add":
        if not program:
            return "Укажите путь к программе для запуска."
        if trigger == "Daily" and not start_time:
            return "Укажите время начала задачи для триггера Daily (формат HH:MM)."

        command = [
            "schtasks", "/create", "/tn", task_name, "/tr", f'"{program}" {arguments}',
            "/sc", trigger
        ]
        if trigger == "Daily" and start_time:
            command.extend(["/st", start_time])
        if description:
            command.extend(["/d", f'"{description}"'])

        try:
            result = subprocess.run(command, capture_output=True, text=True)
            return result.stdout if result.returncode == 0 else result.stderr
        except Exception as e:
            return f"Ошибка при добавлении задачи: {str(e)}"

    elif action == "delete":
        command = ["schtasks", "/delete", "/tn", task_name, "/f"]
        try:
            result = subprocess.run(command, capture_output=True, text=True)
            return result.stdout if result.returncode == 0 else result.stderr
        except Exception as e:
            return f"Ошибка при удалении задачи: {str(e)}"

    elif action == "modify":
        if not program:
            return "Укажите путь к программе для запуска."
        if trigger == "Daily" and not start_time:
            return "Укажите время начала задачи для триггера Daily (формат HH:MM)."

        command = [
            "schtasks", "/change", "/tn", task_name, "/tr", f'"{program}" {arguments}',
            "/sc", trigger
        ]
        if trigger == "Daily" and start_time:
            command.extend(["/st", start_time])
        if description:
            command.extend(["/d", f'"{description}"'])

        try:
            result = subprocess.run(command, capture_output=True, text=True)
            return result.stdout if result.returncode == 0 else result.stderr
        except Exception as e:
            return f"Ошибка при изменении задачи: {str(e)}"

    return "Нет действий для выполнения."