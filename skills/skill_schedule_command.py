NAME = "schedule_command"
DESCRIPTION = "Создает расписание выполнения команд с возможностью указать время и дату для выполнения."
PARAMS = {"command": "команда для выполнения", "time": "время выполнения в формате HH:MM", "date": "дата выполнения в формате YYYY-MM-DD"}
DANGEROUS = False

def run(command="", time="23:59", date="2099-12-31"):
    import os
    import subprocess
    import shlex
    from datetime import datetime

    if not command:
        return "Укажите команду для выполнения."

    if not time or not date:
        return "Укажите время и дату выполнения."

    try:
        dt = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
    except ValueError:
        return "Неверный формат времени или даты."

    current_time = datetime.now()
    if dt < current_time:
        return "Указанное время и дата уже прошли."

    delay_seconds = int((dt - current_time).total_seconds())

    # Windows task scheduler command
    action = f'schtasks /create /tn "ScheduledCommand_{command.replace(" ", "_")}" /tr "{command}" /sc once /st {time} /sd {date} /rl highest'

    try:
        result = subprocess.run(shlex.split(action), capture_output=True, text=True, check=True)
        return f"Задача создана и будет выполнена {date} в {time}."
    except subprocess.CalledProcessError as e:
        return f"Ошибка при создании задачи: {e.stderr}"

    return "Задача создана и будет выполнена в указанное время."