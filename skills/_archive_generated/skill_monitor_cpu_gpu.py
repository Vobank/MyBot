NAME = "monitor_cpu_gpu"
DESCRIPTION = "Показывает информацию о загрузке процессора (CPU) и графического процессора (GPU)."
PARAMS = {}
DANGEROUS = False

def run():
    import os
    import subprocess

    result = []

    try:
        # Получаем информацию о загрузке CPU
        if os.name == 'nt':  # Для Windows
            cpu_info = subprocess.check_output('wmic cpu get loadpercentage', shell=True).decode()
            cpu_load = [line.strip() for line in cpu_info.split('\n') if line.strip().isdigit()]
            if cpu_load:
                result.append(f"CPU Load: {cpu_load[0]}%")
        else:  # Для Linux и macOS
            cpu_load = os.popen("top -bn1 | grep 'Cpu(s)' | sed 's/,/ /g' | awk '{print $2 + $4}'").read().strip()
            result.append(f"CPU Load: {cpu_load}%")

        # Получаем информацию о загрузке GPU
        if os.name == 'nt':  # Для Windows
            gpu_info = subprocess.check_output('nircmd.exe execshell cmd /c "wmic path win32_VideoController get name"', shell=True).decode()
            result.append(f"GPU Info: {gpu_info}")
        else:  # Для Linux
            try:
                gpu_load = subprocess.check_output('nvidia-smi --query-gpu=utilization.gpu --format=csv,noheader,nounits', shell=True).decode().strip()
                result.append(f"GPU Load: {gpu_load}%")
            except Exception as e:
                result.append(f"GPU Load: Не удалось получить информацию. Ошибка: {str(e)}")
    except Exception as e:
        result.append(f"Ошибка: {str(e)}")

    return "\n".join(result)