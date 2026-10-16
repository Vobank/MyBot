NAME = "schedule_manager"
DESCRIPTION = "Управляет расписанием системы: добавляет, изменяет или удаляет задачи."
PARAMS = {
    "action": "действие (add, modify, delete)",
    "task_name": "имя задачи",
    "trigger": "триггер (в формате HH:MM или @daily, @weekly и т.д.)",
    "command": "команда для выполнения (только для добавления)"
}
DANGEROUS = True

def run(action="", task_name="", trigger="", command=""):
    import os
    import subprocess

    if not action or not task_name:
        return "Укажите действие и имя задачи."

    if action.lower() == "add":
        if not trigger or not command:
            return "Для добавления задачи укажите триггер и команду."
        try:
            # Создание задачи через schtasks
            subprocess.run(
                f"schtasks /create /tn \"{task_name}\" /tr \"{command}\" /sc once /st {trigger}",
                check=True,
                capture_output=True,
                shell=True,
                text=True
            )
            return f"Задача \"{task_name}\" добавлена."
        except subprocess.CalledProcessError as e:
            return f"Ошибка при добавлении задачи: {e.stderr}"
    elif action.lower() == "modify":
        if not trigger and not command:
            return "Для изменения задачи укажите триггер или команду."
        try:
            # Изменение задачи через schtasks
            if trigger:
                subprocess.run(
                    f"schtasks /change /tn \"{task_name}\" /st {trigger}",
                    check=True,
                    capture_output=True,
                    shell=True,
                    text=True
                )
            if command:
                subprocess.run(
                    f"schtasks /change /tn \"{task_name}\" /tr \"{command}\"",
                    check=True,
                    capture_output=True,
                    shell=True,
                    text=True
                )
            return f"Задача \"{task_name}\" изменена."
        except subprocess.CalledProcessError as e:
            return f"Ошибка при изменении задачи: {e.stderr}"
    elif action.lower() == "delete":
        try:
            # Удаление задачи через schtasks
            subprocess.run(
                f"schtasks /delete /tn \"{task_name}\" /f",
                check=True,
                capture_output=True,
                shell=True,
                text=True
            )
            return f"Задача \"{task_name}\" удалена."
        except subprocess.CalledProcessError as e:
            return f"Ошибка при удалении задачи: {e.stderr}"
    else:
        return "Неверное действие. Используйте add, modify или delete."