import psutil

NAME = "show_cpu_memory_usage"
DESCRIPTION = "показывает информацию о загруженности CPU и памяти"

def run(text=""):
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_info = psutil.virtual_memory()
    memory_usage = memory_info.percent
    result = f"CPU загружен на {cpu_usage}%\nПамять загружена на {memory_usage}%"
    return result