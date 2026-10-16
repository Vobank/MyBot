import shutil
import os

NAME = "create_backup"
DESCRIPTION = "Создает резервную копию указанной папки."

def run(directory=""):
    if not os.path.isdir(directory):
        return "Указанный путь не является директорией."

    backup_name = f"{directory}_backup"
    try:
        shutil.copytree(directory, backup_name)
        return f"Резервная копия создана: {backup_name}"
    except Exception as e:
        return f"Ошибка при создании резервной копии: {str(e)}"