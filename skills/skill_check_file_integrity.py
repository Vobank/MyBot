NAME = "check_file_integrity"
DESCRIPTION = "Проверяет целостность файлов в папке с помощью контрольной суммы SHA-256."
PARAMS = {"path": "папка (по умолчанию текущая)"}
DANGEROUS = False

def run(path="."):
    import os
    import hashlib

    if not os.path.isdir(path):
        return f"Папка '{path}' не найдена."

    report = []
    for root, _, files in os.walk(path):
        for filename in files:
            file_path = os.path.join(root, filename)
            try:
                with open(file_path, "rb") as f:
                    file_hash = hashlib.sha256(f.read()).hexdigest()
                    report.append(f"{file_path}: {file_hash}")
            except Exception as e:
                report.append(f"Ошибка при чтении {file_path}: {str(e)}")
    
    return "\n".join(report) if report else "Нет файлов для проверки."