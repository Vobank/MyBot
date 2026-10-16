import schedule
import time
import subprocess

NAME = "schedule_task_with_time"
DESCRIPTION = "Создание и управление задачами по расписанию с возможностью указания даты и времени."

def run(text=""):
    try:
        command, date_time = text.split(' ', 1)
        date_time = date_time.strip()
        schedule.every().day.at(date_time).do(subprocess.run, command, shell=True)
        return "Задача расписана на время: " + date_time
    except ValueError:
        return "Неверный формат команды. Используйте: команда время (например, 'ls 15:30')"

def job():
    while True:
        schedule.run_pending()
        time.sleep(1)

# Запуск задач
import threading
thread = threading.Thread(target=job)
thread.start()