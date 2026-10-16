NAME = "cpu_energy_monitor"
DESCRIPTION = "Отслеживает и контролирует использование энергии процессором в реальном времени."
PARAMS = {"interval": "интервал между измерениями (секунды)", "duration": "общая длительность мониторинга (секунды)"}
DANGEROUS = False

def run(interval=5, duration=60):
    import os
    import time
    import psutil

    if interval <= 0:
        return "Интервал должен быть больше 0."
    if duration <= 0:
        return "Длительность должна быть больше 0."
    
    result = []
    end_time = time.time() + duration
    
    while time.time() < end_time:
        energy_usage = psutil.cpu_percent(interval=interval)
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        result.append(f"{timestamp}: {energy_usage}%")
        if time.time() + interval > end_time:
            break
    
    return "\n".join(result) if result else "Нет данных по энергопотреблению процессора."