NAME = "keyboard_settings_manager"
DESCRIPTION = "Управляет настройками клавиатуры: повторение и скорость нажатия."
PARAMS = {"repeat_delay": "задержка повторения клавиш в мс (0-1200)", "repeat_rate": "скорость повторения клавиш в мс (0-31)"}
DANGEROUS = True

def run(repeat_delay=None, repeat_rate=None):
    import os
    import subprocess

    if repeat_delay is None and repeat_rate is None:
        return "Укажи параметры для изменения: repeat_delay и/или repeat_rate."
    
    if repeat_delay is not None:
        repeat_delay = max(0, min(1200, int(repeat_delay)))
        subprocess.run(["powershell", "-Command", f"(Get-ItemProperty -Path 'HKCU:\\Control Panel\\Keyboard').KeyboardDelay = {repeat_delay}"])
    
    if repeat_rate is not None:
        repeat_rate = max(0, min(31, int(repeat_rate)))
        subprocess.run(["powershell", "-Command", f"(Get-ItemProperty -Path 'HKCU:\\Control Panel\\Keyboard').KeyboardSpeed = {repeat_rate}"])

    return "Настройки клавиатуры обновлены."