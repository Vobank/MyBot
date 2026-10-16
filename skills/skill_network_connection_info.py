NAME = "network_connection_info"
DESCRIPTION = "Показывает информацию о текущих сетевых подключениях и их статусе."
PARAMS = {}

def run():
    import subprocess

    try:
        # Получаем информацию о сетевых подключениях с помощью команды netsh
        result = subprocess.run(["netsh", "interface", "show", "interface"], capture_output=True, text=True, check=True)
        output = result.stdout

        # Форматируем вывод для удобства чтения
        lines = output.splitlines()
        formatted_output = "\n".join(lines[3:])
        return formatted_output
    except subprocess.CalledProcessError as e:
        return f"Произошла ошибка при выполнении команды: {e.stderr}"
    except Exception as e:
        return f"Произошла ошибка: {str(e)}"