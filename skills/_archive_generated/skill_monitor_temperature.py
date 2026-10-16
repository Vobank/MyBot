import os
import subprocess

NAME = "monitor_temperature"
DESCRIPTION = "Мониторит и отображает температуру компонентов ПК"

def run(text=""):
    try:
        # Используем sensors из lm_sensors для получения температуры
        result = subprocess.run(['sensors'], stdout=subprocess.PIPE)
        output = result.stdout.decode()
        return output
    except Exception as e:
        return f"Ошибка при получении данных о температуре: {str(e)}"