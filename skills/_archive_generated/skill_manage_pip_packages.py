NAME = "manage_pip_packages"
DESCRIPTION = "Устанавливает, обновляет и удаляет пакеты через pip."

def run(action, package_name=""):
    import subprocess

    if action == "install":
        command = ["pip", "install", package_name]
        message = f"Установка пакета {package_name}..."
    elif action == "update":
        command = ["pip", "install", "--upgrade", package_name]
        message = f"Обновление пакета {package_name}..."
    elif action == "uninstall":
        command = ["pip", "uninstall", "-y", package_name]
        message = f"Удаление пакета {package_name}..."
    else:
        return "Неизвестное действие."

    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        message += "\nУспешно!"
    except subprocess.CalledProcessError as e:
        message += f"\nОшибка: {e.stderr}"

    return message