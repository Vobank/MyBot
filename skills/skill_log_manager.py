import os
import subprocess

NAME = "log_manager"
DESCRIPTION = "Управление логами и сохранение ошибок для последующего анализа"

def run(text=""):
    command = text.strip()
    if not command:
        return "Пожалуйста, укажите команду для выполнения."
    
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = result.stdout.decode()
        error = result.stderr.decode()
        if error:
            log_file_path = os.path.join(os.getcwd(), "error_log.txt")
            with open(log_file_path, "a") as log_file:
                log_file.write(f"Command: {command}\nError: {error}\n{'-'*40}\n")
            return f"Команда выполнена с ошибкой. Ошибка сохранена в {log_file_path}."
        else:
            return f"Команда выполнена успешно:\n{output}"
    except subprocess.CalledProcessError as e:
        log_file_path = os.path.join(os.getcwd(), "error_log.txt")
        with open(log_file_path, "a") as log_file:
            log_file.write(f"Command: {command}\nError: {str(e)}\n{'-'*40}\n")
        return f"Команда не выполнена успешно. Ошибка сохранена в {log_file_path}."