import os
import shutil

NAME = "file_version_manager"
DESCRIPTION = "Создает резервные копии файлов с добавлением суффикса версии"

def run(file_path=""):
    if not os.path.exists(file_path):
        return "Файл не найден."

    file_dir, file_name = os.path.split(file_path)
    base_name, extension = os.path.splitext(file_name)
    version = 1
    new_file_name = f"{base_name}_v{version}{extension}"
    new_file_path = os.path.join(file_dir, new_file_name)

    while os.path.exists(new_file_path):
        version += 1
        new_file_name = f"{base_name}_v{version}{extension}"
        new_file_path = os.path.join(file_dir, new_file_name)

    shutil.copy2(file_path, new_file_path)
    return f"Создана резервная копия файла: {new_file_path}"