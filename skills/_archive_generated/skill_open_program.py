NAME = "open_program"
DESCRIPTION = "Открывает указанную программу (по полному пути или имени)."
PARAMS = {"program_path": "Полный путь к программе или её имя"}
DANGEROUS = False

def run(program_path=""):
    import subprocess
    import os

    if not program_path:
        return "Укажи, какую программу нужно открыть."

    try:
        if os.path.isfile(program_path):
            subprocess.Popen([program_path])
            return f"Программа {program_path} успешно открыта."
        else:
            # Попробуем открыть программу по имени
            subprocess.Popen(program_path)
            return f"Программа {program_path} успешно открыта."
    except Exception as e:
        return f"Не удалось открыть программу: {str(e)}"