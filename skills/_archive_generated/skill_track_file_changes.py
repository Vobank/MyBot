import os
import hashlib

NAME = "track_file_changes"
DESCRIPTION = "Отслеживает изменения в файлах проекта"

def get_file_hash(file_path):
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

def run(project_path=""):
    if not os.path.isdir(project_path):
        return "Указанная директория проекта не существует."
    
    changes = {}
    for root, dirs, files in os.walk(project_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_hash = get_file_hash(file_path)
            changes[file_path] = file_hash
    
    # Здесь можно сохранить хеши в файл или базу данных для последующего сравнения
    return "Отслеживание изменений в файлах проекта выполнено."