import subprocess
import os
import re

NAME = "task_scheduler"
DESCRIPTION = "Создание и управление задачами по расписанию"

def run(text=""):
    command = text.lower()
    if "создать задачу" in command:
        # Пример команды: создать задачу "python script.py" каждые 24 часа
        match = re.match(r'создать задачу "(.*)" каждые (\d+) (часа|минуты|секунды)', command)
        if match:
            task_command = match.group(1)
            interval = match.group(2)
            unit = match.group(3)
            schedule_type = "hour" if unit == "часа" else ("minute" if unit == "минуты" else "second")
            task_name = f"mybot_task_{task_command.replace(' ', '_')}"
            cron_command = f"*/{interval} * * * * {task_command}"
            # Создание cron-задачи
            with open('/etc/cron.d/mybot', 'a') as cron_file:
                cron_file.write(f"{cron_command} # {task_name}\n")
            return f"Задача '{task_name}' создана и будет выполняться каждые {interval} {unit}."
        else:
            return "Неверный формат команды. Используйте 'создать задачу \"команда\" каждые n интервал'."
    elif "удалить задачу" in command:
        # Пример команды: удалить задачу "python script.py"
        match = re.match(r'удалить задачу "(.*)"', command)
        if match:
            task_command = match.group(1)
            task_name = f"mybot_task_{task_command.replace(' ', '_')}"
            # Удаление cron-задачи
            with open('/etc/cron.d/mybot', 'r') as cron_file:
                lines = cron_file.readlines()
            with open('/etc/cron.d/mybot', 'w') as cron_file:
                for line in lines:
                    if task_name not in line:
                        cron_file.write(line)
            return f"Задача '{task_name}' удалена."
        else:
            return "Неверный формат команды. Используйте 'удалить задачу \"команда\"'."
    else:
        return "Команда не распознана. Используйте 'создать задачу' или 'удалить задачу'."