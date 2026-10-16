NAME = "backup_file"
DESCRIPTION = "Создает резервную копию указанного файла в указанную папку."
PARAMS = {"file_path": "путь к файлу", "backup_dir": "путь к папке для резервной копии"}
DANGEROUS = False

def run(file_path="", backup_dir="backups"):
    import os
    import shutil

    if not file_path:
        return "Укажи путь к файлу."

    if not os.path.exists(file_path):
        return "Файл не существует."

    os.makedirs(backup_dir, exist_ok=True)

    backup_file_path = os.path.join(backup_dir, os.path.basename(file_path))

    try:
        shutil.copy2(file_path, backup_file_path)
        return f"Резервная копия успешно создана в {backup_file_path}."
    except Exception as e:
        return f"Ошибка при создании резервной копии: {str(e)}"