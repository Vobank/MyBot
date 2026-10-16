import os
import shutil
import time

NAME = "project_backup"
DESCRIPTION = "Создание и управление резервными копиями проектов"

def run(text=""):
    project_path = text.strip()
    if not project_path:
        return "Пожалуйста, укажите путь к проекту."
    
    if not os.path.isdir(project_path):
        return "Указанный путь не является директорией проекта."
    
    backup_dir = os.path.join(os.path.dirname(project_path), f"{os.path.basename(project_path)}_backup_{int(time.time())}")
    
    try:
        shutil.copytree(project_path, backup_dir)
        return f"Резервная копия проекта создана в {backup_dir}"
    except Exception as e:
        return f"Не удалось создать резервную копию: {str(e)}"