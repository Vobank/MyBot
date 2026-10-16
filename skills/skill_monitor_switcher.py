NAME = "monitor_switcher"
DESCRIPTION = "Автоматически переключается между мониторами в зависимости от времени суток."
PARAMS = {"start_time": "время начала работы (например, '09:00')", "end_time": "время окончания работы (например, '18:00')"}
DANGEROUS = True

def run(start_time="09:00", end_time="18:00"):
    import os
    from datetime import datetime

    def switch_monitor(state):
        try:
            # Пример команды для переключения монитора в Windows (для примера)
            if state == "on":
                os.system("powershell Set-DisplayMode -DeviceName 'Display1' -Mode 'Extend'")
            elif state == "off":
                os.system("powershell Set-DisplayMode -DeviceName 'Display1' -Mode 'Duplicate'")
        except Exception as e:
            return f"Ошибка при переключении монитора: {str(e)}"
        return "Монитор успешно переключен."

    now = datetime.now().time()
    start = datetime.strptime(start_time, "%H:%M").time()
    end = datetime.strptime(end_time, "%H:%M").time()

    if start <= now <= end:
        return switch_monitor("on")
    else:
        return switch_monitor("off")