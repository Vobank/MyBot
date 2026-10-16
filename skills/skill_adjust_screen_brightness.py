NAME = "adjust_screen_brightness"
DESCRIPTION = "Автоматически изменяет яркость экрана в зависимости от времени суток."
PARAMS = {"brightness_morning": "Уровень яркости утром (0-100)", "brightness_night": "Уровень яркости вечером (0-100)"}
DANGEROUS = False

def run(brightness_morning=70, brightness_night=30):
    import datetime
    import os
    import subprocess

    # Определяем текущее время
    current_time = datetime.datetime.now().time()

    # Определяем время утра и вечера
    morning_time = datetime.time(6, 0)
    night_time = datetime.time(20, 0)

    # Определяем текущую яркость экрана
    current_brightness = subprocess.run(['powershell', '-Command', '(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightness).CurrentBrightness'], capture_output=True, text=True).stdout.strip()

    # Изменяем яркость в зависимости от времени суток
    if current_time >= morning_time and current_time < night_time:
        target_brightness = brightness_morning
    else:
        target_brightness = brightness_night

    # Установка яркости экрана
    try:
        subprocess.run(['powershell', '-Command', f'(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1, {target_brightness})'], check=True)
        return f"Яркость экрана установлена на {target_brightness}%."
    except subprocess.CalledProcessError as e:
        return f"Ошибка при изменении яркости экрана: {e}"