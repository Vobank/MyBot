NAME = "time_stamped_backup"
DESCRIPTION = "Создает копию указанного файла в папке с текущей датой и временем в имени файла."
PARAMS = {"file_path": "путь к файлу", "backup_dir": "папка для резервной копии (по умолчанию в той же папке)"}
def run(file_path="", backup_dir=""):
    import os
    import shutil
    from datetime import datetime

    if not file_path:
        return "Укажите путь к файлу."

    if not os.path.isfile(file_path):
        return "Файл не существует."

    if not backup_dir:
        backup_dir = os.path.dirname(file_path)

    try:
        file_name = os.path.basename(file_path)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file_name = f"{os.path.splitext(file_name)[0]}_{timestamp}{os.path.splitext(file_name)[1]}"
        backup_file_path = os.path.join(backup_dir, backup_file_name)

        shutil.copy2(file_path, backup_file_path)
        return f"Копия файла создана: {backup_file_path}"
    except Exception as e:
        return f"Произошла ошибка при создании резервной копии: {str(e)}"