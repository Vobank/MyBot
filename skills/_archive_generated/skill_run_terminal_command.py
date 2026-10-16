NAME = "run_terminal_command"
DESCRIPTION = "Выполняет указанную команду в терминале и возвращает результат."
PARAMS = {"command": "команда, которую нужно выполнить"}
def run(command=""):
    if not command:
        return "Укажи команду для выполнения."
    import subprocess
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return f"Выходные данные:\n{result.stdout}\nОшибки:\n{result.stderr}"
    except subprocess.CalledProcessError as e:
        return f"Команда завершилась с ошибкой:\n{e.stderr}"
    except Exception as e:
        return f"Произошла ошибка:\n{str(e)}"