import os
import psutil

NAME = "show_active_processes"
DESCRIPTION = "Отображает список активных процессов на ПК"

def run(text=""):
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        processes.append(f"PID: {proc.info['pid']}, Name: {proc.info['name']}, CPU: {proc.info['cpu_percent']}%, Memory: {proc.info['memory_percent']}%")
    return "\n".join(processes)