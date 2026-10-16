import os
import subprocess

NAME = "window_switcher"
DESCRIPTION = "Управление окнами приложений и переключение между ними."

def run(text=""):
    if text.lower() == "next":
        subprocess.run(["wmctrl", "-a", ":NEXT"])
        return "Переключение на следующее окно."
    elif text.lower() == "previous":
        subprocess.run(["wmctrl", "-a", ":PREV"])
        return "Переключение на предыдущее окно."
    elif text:
        app_name = text
        subprocess.run(["wmctrl", "-a", app_name])
        return f"Переключение на окно приложения: {app_name}"
    else:
        return "Необходимо указать имя приложения или 'next'/'previous' для переключения между окнами."