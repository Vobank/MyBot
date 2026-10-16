import os
import subprocess

NAME = "process_manager"
DESCRIPTION = "Управление и мониторинг процессов на ПК, включая возможность убивать процессы."

def run(text=""):
    command = text.lower().strip()

    if command == "show":
        return show_active_processes()
    elif "kill" in command:
        pid = command.split(' ')[1]
        return kill_process(pid)
    else:
        return "Неизвестная команда. Используйте 'show' для отображения процессов или 'kill [pid]' для убивания процесса."

def show_active_processes():
    result = subprocess.run(['tasklist'], capture_output=True, text=True)
    return result.stdout

def kill_process(pid):
    try:
        os.system(f'taskkill /F /PID {pid}')
        return f"Процесс с PID {pid} был успешно убит."
    except Exception as e:
        return f"Произошла ошибка при попытке убить процесс: {str(e)}"