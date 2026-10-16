NAME = "network_connections_report"
DESCRIPTION = "Создает отчет о активных сетевых соединениях и открытых портах."
PARAMS = {"include_listening_ports": "если True, включает в отчет слушающие порты"}
DANGEROUS = False

def run(include_listening_ports=True):
    import subprocess
    try:
        result = subprocess.run(['netstat', '-ano'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        connections = result.stdout.splitlines()
        
        listening_ports = []
        if include_listening_ports:
            result = subprocess.run(['netstat', '-an'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
            listening_ports = result.stdout.splitlines()
            
        report = "Активные сетевые соединения:\n"
        report += "\n".join(connections) + "\n"
        
        if include_listening_ports:
            report += "\nСлушающие порты:\n"
            report += "\n".join(listening_ports) + "\n"
        
        return report
    except Exception as e:
        return f"Не удалось получить информацию о сетевых соединениях: {str(e)}"