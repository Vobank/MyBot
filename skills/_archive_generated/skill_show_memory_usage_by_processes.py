import os
import psutil

NAME = "show_memory_usage_by_processes"
DESCRIPTION = "Показывает статистику использования памяти на уровне процессов."

def run(text=""):
    memory_info = []
    for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
        pid = proc.info['pid']
        name = proc.info['name']
        memory_info.append((pid, name, proc.info['memory_info'].rss))
    
    result = "Статистика использования памяти:\n"
    for pid, name, rss in sorted(memory_info, key=lambda x: x[2], reverse=True)[:10]:
        result += f"PID: {pid}, Name: {name}, Memory Usage: {rss / (1024 * 1024):.2f} MB\n"
    
    return result