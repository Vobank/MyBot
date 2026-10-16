NAME = "network_ports_info"
DESCRIPTION = "Показывает информацию о доступных и использованных сетевых портах."
PARAMS = {}
DANGEROUS = False

def run():
    import subprocess

    try:
        result = subprocess.run(["netstat", "-an"], capture_output=True, text=True, check=True)
        lines = result.stdout.strip().split('\n')
        if not lines:
            return "Нет информации о сетевых портах."
        
        header = lines[0]
        info = lines[1:]
        return f"{header}\n{'-'*len(header)}\n" + "\n".join(info[:100]) + ("\n... (обрезано)" if len(info) > 100 else "")
    
    except subprocess.CalledProcessError as e:
        return f"Ошибка выполнения команды: {e.stderr}"
    except Exception as e:
        return f"Произошла ошибка: {str(e)}"