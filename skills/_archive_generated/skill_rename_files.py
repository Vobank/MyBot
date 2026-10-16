import os

NAME = "rename_files"
DESCRIPTION = "Переименовывает файлы в указанной директории, добавляя префикс или суффикс к их именам."

def run(text=""):
    if not text:
        return "Необходимо указать директорию и префикс или суффикс для переименования файлов."
    
    parts = text.split()
    if len(parts) < 2:
        return "Необходимо указать директорию и префикс или суффикс для переименования файлов."
    
    directory = parts[0]
    prefix_suffix = ' '.join(parts[1:])
    
    if not os.path.isdir(directory):
        return f"Директория {directory} не существует."
    
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            new_filename = f"{prefix_suffix}{filename}" if prefix_suffix.startswith('.') else f"{filename}{prefix_suffix}"
            new_file_path = os.path.join(directory, new_filename)
            os.rename(file_path, new_file_path)
    
    return f"Файлы в директории {directory} успешно переименованы."