NAME = "service_manager"
DESCRIPTION = "Запускает или останавливает службу Windows по расписанию."
PARAMS = {
    "service_name": "имя службы",
    "action": "действие (start или stop)",
    "schedule": "время в формате 'HH:MM' или 'now' для немедленного выполнения"
}
DANGEROUS = True

def run(service_name="", action="", schedule="now"):
    import os
    import subprocess
    import time
    from datetime import datetime

    if not service_name or not action:
        return "Укажи имя службы и действие (start или stop)."

    if action not in ["start", "stop"]:
        return "Действие должно быть 'start' или 'stop'."

    if schedule != "now":
        try:
            schedule_time = datetime.strptime(schedule, "%H:%M")
            current_time = datetime.now().time()
            schedule_time = schedule_time.replace(
                year=current_time.year,
                month=current_time.month,
                day=current_time.day
            )
            if schedule_time.time() <= current_time:
                schedule_time += timedelta(days=1)
            time_to_wait = (schedule_time - datetime.now()).total_seconds()
            time.sleep(time_to_wait)
        except ValueError:
            return "Неверный формат времени. Используй формат 'HH:MM' или 'now'."

    try:
        if action == "start":
            subprocess.run(["sc", "start", service_name], check=True)
        elif action == "stop":
            subprocess.run(["sc", "stop", service_name], check=True)
        return f"Служба {service_name} успешно {action}ed."
    except subprocess.CalledProcessError as e:
        return f"Ошибка при {action}ing службы {service_name}: {e}"