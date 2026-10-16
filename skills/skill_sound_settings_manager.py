NAME = "sound_settings_manager"
DESCRIPTION = "Управляет настройками звука на ПК: уровень громкости, выбор устройства воспроизведения."
PARAMS = {"action": "действие (increase, decrease, set, list_devices, select_device)", "value": "значение (для increase, decrease, set) или имя устройства (для select_device)"}
DANGEROUS = False

def run(action="list_devices", value=""):
    import os, subprocess

    def list_devices():
        result = subprocess.run(['powershell', '-Command', '(Get-AudioDevice -Playback -Default).Name'], capture_output=True, text=True)
        return f"Текущее устройство воспроизведения: {result.stdout.strip()}"

    def set_volume(level):
        if not (0 <= int(level) <= 100):
            return "Уровень громкости должен быть от 0 до 100."
        subprocess.run(['nircmd', 'setsysvolume', str(int(level) * 65536 // 100)])
        return f"Уровень громкости установлен на {level}%."

    def increase_volume(steps=10):
        subprocess.run(['nircmd', 'changesysvolume', str(steps * 65536 // 100)])
        return f"Уровень громкости увеличен на {steps}%."

    def decrease_volume(steps=10):
        subprocess.run(['nircmd', 'changesysvolume', str(-steps * 65536 // 100)])
        return f"Уровень громкости уменьшен на {steps}%."

    def select_device(device_name):
        result = subprocess.run(['powershell', '-Command', f'(Get-AudioDevice -Playback | Where-Object {{ $_.Name -eq "{device_name}" }}).Name'], capture_output=True, text=True)
        if result.stdout.strip() == device_name:
            subprocess.run(['powershell', '-Command', f'Set-AudioDevice -Playback -Name "{device_name}"'])
            return f"Устройство воспроизведения установлено на {device_name}."
        else:
            return f"Устройство {device_name} не найдено."

    try:
        if action == "list_devices":
            return list_devices()
        elif action == "set":
            return set_volume(value)
        elif action == "increase":
            return increase_volume(int(value) if value else 10)
        elif action == "decrease":
            return decrease_volume(int(value) if value else 10)
        elif action == "select_device":
            return select_device(value)
        else:
            return "Неверное действие. Используйте одно из: increase, decrease, set, list_devices, select_device."
    except Exception as e:
        return f"Произошла ошибка: {str(e)}"