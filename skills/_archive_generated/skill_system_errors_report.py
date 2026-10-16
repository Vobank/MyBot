NAME = "system_errors_report"
DESCRIPTION = "Создает отчет о системных ошибках и предупреждениях."
PARAMS = {"path": "путь к лог-файлу (по умолчанию C:\\Windows\\System32\\df.exe /T)"}
DANGEROUS = False

def run(path="C:\\Windows\\System32\\df.exe /T"):
    import os
    import subprocess

    if not os.path.exists(path):
        return "Указанный путь не существует."

    try:
        result = subprocess.run(["df.exe", "/T"], capture_output=True, text=True, check=True)
        errors = []
        for line in result.stdout.splitlines():
            if "error" in line.lower() or "warning" in line.lower():
                errors.append(line.strip())
        
        return "\n".join(errors) if errors else "Нет системных ошибок или предупреждений."
    except subprocess.CalledProcessError as e:
        return f"Произошла ошибка при выполнении команды: {e.stderr}"
    except Exception as e:
        return f"Произошла непредвиденная ошибка: {str(e)}"