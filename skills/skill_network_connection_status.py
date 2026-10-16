NAME = "network_connection_status"
DESCRIPTION = "Показывает текущее состояние сетевых подключений и подсвечивает активные соединения."
PARAMS = {}
DANGEROUS = False

def run():
    import os
    import subprocess

    try:
        # Получаем состояние сетевых подключений
        result = subprocess.run(["netstat", "-an"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        connections = result.stdout.splitlines()

        # Фильтруем активные соединения
        active_connections = [line for line in connections if "ESTABLISHED" in line]

        # Формируем результат
        result_str = "Состояние сетевых подключений:\n\n"
        for line in connections:
            if line in active_connections:
                result_str += f"> {line}\n"  # Подсветка активных соединений
            else:
                result_str += f"  {line}\n"

        return result_str

    except subprocess.CalledProcessError as e:
        return f"Ошибка при выполнении команды: {e.stderr}"
    except Exception as e:
        return f"Произошла ошибка: {str(e)}"