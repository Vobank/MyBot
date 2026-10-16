import subprocess

NAME = "manage_python_packages"
DESCRIPTION = "Управляет установкой и удалением пакетов Python"

def run(text=""):
    command = text.lower()
    if "install" in command:
        package_name = command.replace("install ", "").strip()
        if package_name:
            result = subprocess.run(['pip', 'install', package_name], capture_output=True, text=True)
            return result.stdout + result.stderr
        else:
            return "Имя пакета не указано"
    elif "uninstall" in command:
        package_name = command.replace("uninstall ", "").strip()
        if package_name:
            result = subprocess.run(['pip', 'uninstall', '-y', package_name], capture_output=True, text=True)
            return result.stdout + result.stderr
        else:
            return "Имя пакета не указано"
    else:
        return "Неизвестная команда. Используйте 'install <имя>' или 'uninstall <имя>'"