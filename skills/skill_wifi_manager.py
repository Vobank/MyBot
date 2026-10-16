NAME = "wifi_manager"
DESCRIPTION = "Управляет настройками Wi-Fi: подключение, отключение, информация о подключении."
PARAMS = {"action": "действие (connect, disconnect, info)", "ssid": "название Wi-Fi сети (только для connect)", "password": "пароль Wi-Fi (только для connect)"}
DANGEROUS = False

def run(action="info", ssid="", password=""):
    import subprocess

    if action not in ["connect", "disconnect", "info"]:
        return "Действие должно быть 'connect', 'disconnect' или 'info'."

    try:
        if action == "info":
            result = subprocess.run(["netsh", "wlan", "show", "interfaces"], capture_output=True, text=True)
            return result.stdout

        if action == "connect":
            if not ssid or not password:
                return "Для подключения укажите название сети (ssid) и пароль."
            result = subprocess.run(["netsh", "wlan", "connect", "name={}".format(ssid), "keyMaterial={}".format(password)], capture_output=True, text=True)
            return result.stdout

        if action == "disconnect":
            result = subprocess.run(["netsh", "wlan", "disconnect"], capture_output=True, text=True)
            return result.stdout

    except Exception as e:
        return f"Произошла ошибка: {str(e)}"

    return "Действие выполнено."