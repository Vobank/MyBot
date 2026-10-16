import subprocess

NAME = "run_command"
DESCRIPTION = "Выполняет команду командной строки и возвращает результат."

def run(text=""):
    try:
        result = subprocess.run(text, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.stdout.decode('utf-8') + result.stderr.decode('utf-8')
    except subprocess.CalledProcessError as e:
        return f"Ошибка выполнения команды: {e.stderr.decode('utf-8')}"