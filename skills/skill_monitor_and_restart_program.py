NAME = "monitor_and_restart_program"
DESCRIPTION = "Запускает указанную программу по расписанию и контролирует её выполнение, автоматически перезапуская при необходимости."
PARAMS = {"program_path": "путь к исполняемому файлу", "interval": "интервал проверки в секундах", "duration": "общее время работы в секундах"}
DANGEROUS = False

def run(program_path="", interval=60, duration=3600):
    import os
    import time
    import subprocess
    import psutil

    if not program_path:
        return "Укажи путь к программе."

    def is_running(process_name):
        for proc in psutil.process_iter(['name']):
            if proc.info['name'] == process_name:
                return True
        return False

    start_time = time.time()
    program_name = os.path.basename(program_path)

    while (time.time() - start_time) < duration:
        if not is_running(program_name):
            subprocess.Popen(program_path)
            return_value = f"Программа {program_name} перезапущена."
        else:
            return_value = f"Программа {program_name} работает."

        time.sleep(interval)

    return return_value