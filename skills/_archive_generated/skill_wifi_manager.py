NAME = "wifi_manager"
DESCRIPTION = "Управляет настройками Wi-Fi сети: включает, выключает и показывает информацию о текущей сети."
PARAMS = {"action": "действие (on/off/info)", "ssid": "имя сети (только для подключения)", "password": "пароль (только для подключения)"}
DANGEROUS = True

def run(action="info", ssid="", password=""):
    import subprocess
    import re

    if action == "on":
        result = subprocess.run(["netsh", "interface", "set", "interface", "name='Wi-Fi'", "admin=enabled"], capture_output=True, text=True)
        return "Wi-Fi включен." if "successfully" in result.stdout.lower() else "Не удалось включить Wi-Fi."
    
    elif action == "off":
        result = subprocess.run(["netsh", "interface", "set", "interface", "name='Wi-Fi'", "admin=disabled"], capture_output=True, text=True)
        return "Wi-Fi выключен." if "successfully" in result.stdout.lower() else "Не удалось выключить Wi-Fi."
    
    elif action == "info":
        result = subprocess.run(["netsh", "wlan", "show", "interfaces"], capture_output=True, text=True)
        lines = result.stdout.splitlines()
        ssid_line = next((line for line in lines if "SSID" in line), "")
        ssid = ssid_line.split(":")[-1].strip() if ssid_line else "Не подключен"
        status_line = next((line for line in lines if "State" in line), "")
        status = status_line.split(":")[-1].strip() if status_line else "Неизвестно"
        return f"Wi-Fi: {status}, Сеть: {ssid}"
    
    elif action == "connect":
        result = subprocess.run(["netsh", "wlan", "connect", "name={}".format(ssid)], capture_output=True, text=True)
        if "could not connect" in result.stderr.lower():
            return "Не удалось подключиться к Wi-Fi."
        return f"Подключение к Wi-Fi '{ssid}' установлено."
    
    else:
        return "Неизвестное действие. Используйте on/off/info/connect."