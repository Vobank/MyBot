NAME = "network_connection"
DESCRIPTION = "Подключает или отключает сетевое подключение по его имени."
PARAMS = {"action": "подключить или отключить", "connection_name": "имя сетевого подключения"}
DANGEROUS = True

def run(action="подключить", connection_name="Ethernet"):
    import subprocess

    if action not in ["подключить", "отключить"]:
        return "Действие должно быть 'подключить' или 'отключить'."
    
    if not connection_name:
        return "Укажи имя сетевого подключения."
    
    try:
        if action == "подключить":
            result = subprocess.run(['netsh', 'interface', 'set', 'interface', 'name="{}"'.format(connection_name), 'admin', 'on'], capture_output=True, text=True)
        else:
            result = subprocess.run(['netsh', 'interface', 'set', 'interface', 'name="{}"'.format(connection_name), 'admin', 'off'], capture_output=True, text=True)

        if result.returncode != 0:
            return "Ошибка: " + result.stderr
        else:
            return "Успешно " + action + "ено подключение " + connection_name + "."
    except Exception as e:
        return "Произошла ошибка: " + str(e)