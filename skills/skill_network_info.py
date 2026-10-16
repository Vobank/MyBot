NAME = "network_info"
DESCRIPTION = "Показывает информацию о сети и подключенных интерфейсах."
PARAMS = {}
DANGEROUS = False

def run():
    import os
    import socket
    import subprocess

    try:
        # Получение информации о сетевых интерфейсах
        interfaces = []
        for line in subprocess.check_output("ipconfig", shell=True).decode().split("\n"):
            if "adapter" in line:
                interface_name = line.split(":")[1].strip()
            elif "IPv4 Address" in line:
                ipv4_address = line.split(":")[1].strip()
                interfaces.append((interface_name, ipv4_address))
        
        # Получение информации о хосте
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)

        # Формирование результата
        result = f"Информация о сети:\n"
        result += f"Хост: {hostname} ({ip_address})\n"
        result += "Интерфейсы:\n"
        for interface, ip in interfaces:
            result += f"  - {interface}: {ip}\n"
        
        return result
    except Exception as e:
        return f"Ошибка при получении информации о сети: {str(e)}"