NAME = "program_controller"
DESCRIPTION = "запускает и закрывает программы по запросу"

def run(text=""):
    import subprocess
    import os

    commands = text.split()
    if len(commands) < 2:
        return "Пожалуйста, укажите действие (запустить/закрыть) и название программы."

    action, program = commands[0], commands[1]

    if action == "запустить":
        try:
            subprocess.Popen(program)
            return f"Программа {program} запущена."
        except Exception as e:
            return f"Не удалось запустить программу {program}: {str(e)}"
    elif action == "закрыть":
        os.system(f'taskkill /F /IM {program}.exe')
        return f"Программа {program} закрыта."
    else:
        return "Действие не распознано. Используйте 'запустить' или 'закрыть'."