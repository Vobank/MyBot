NAME = "scheduled_task"
DESCRIPTION = "Запускает указанную программу по заданному расписанию."
PARAMS = {
    "program": "путь к программе или её имя",
    "time": "время запуска в формате HH:MM"
}
DANGEROUS = False

def run(program="", time=""):
    import os
    import time as tm
    from datetime import datetime

    if not program:
        return "Укажи программу для запуска."
    if not time:
        return "Укажи время запуска в формате HH:MM."

    try:
        hour, minute = map(int, time.split(':'))
        if hour < 0 or hour > 23 or minute < 0 or minute > 59:
            return "Неверный формат времени. Используй HH:MM."
    except ValueError:
        return "Неверный формат времени. Используй HH:MM."

    now = datetime.now()
    target_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    if target_time <= now:
        target_time += tm.timedelta(days=1)

    time_to_wait = (target_time - now).total_seconds()
    tm.sleep(time_to_wait)

    if os.name == 'nt':
        os.system(f'start "" "{program}"')
    else:
        os.system(f'nohup {program} &> /dev/null &')

    return f"Программа {program} будет запущена в {time}."