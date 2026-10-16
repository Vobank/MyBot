import subprocess
import os

NAME = "window_controller"
DESCRIPTION = "управление окнами приложений и переключение между ними по названию"

def run(text=""):
    command = text.lower()
    if "switch" in command:
        app_name = command.split("switch ")[-1]
        try:
            subprocess.run(["xdotool", "search", "--onlyvisible", "--name", app_name, "windowactivate"], check=True)
            return f"Переключение на окно {app_name} выполнено."
        except subprocess.CalledProcessError as e:
            return f"Не удалось переключиться на окно {app_name}. Ошибка: {str(e)}"
    elif "close" in command:
        app_name = command.split("close ")[-1]
        try:
            subprocess.run(["xdotool", "search", "--onlyvisible", "--name", app_name, "windowkill"], check=True)
            return f"Окно {app_name} закрыто."
        except subprocess.CalledProcessError as e:
            return f"Не удалось закрыть окно {app_name}. Ошибка: {str(e)}"
    else:
        return "Команда не распознана. Используйте 'switch <название окна>' или 'close <название окна>'."