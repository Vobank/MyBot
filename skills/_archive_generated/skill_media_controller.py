import subprocess
import os

NAME = "media_controller"
DESCRIPTION = "воспроизводить и останавливать музыку/видео в проигрывателе"

def run(action=""):
    if action.lower() not in ["play", "pause", "stop"]:
        return "Недопустимое действие. Используйте 'play', 'pause' или 'stop'."

    command = {
        "play": "xdotool key Play",
        "pause": "xdotool key Pause",
        "stop": "xdotool key Stop"
    }

    try:
        subprocess.run(command[action], shell=True, check=True)
        return f"Действие '{action}' выполнено."
    except subprocess.CalledProcessError as e:
        return f"Ошибка при выполнении действия '{action}': {str(e)}"