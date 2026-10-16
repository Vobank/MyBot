import psutil

NAME = "show_system_status"
DESCRIPTION = "Показывает статус загрузки CPU и памяти на ПК."

def run(text=""):
    cpu_percent = psutil.cpu_percent(interval=1)
    memory_info = psutil.virtual_memory()
    memory_percent = memory_info.percent
    result = f"Загрузка CPU: {cpu_percent}%\nЗагрузка памяти: {memory_percent}%"
    return result