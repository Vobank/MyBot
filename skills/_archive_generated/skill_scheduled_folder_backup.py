NAME = "scheduled_folder_backup"
DESCRIPTION = "Создает автоматическое резервное копирование всех файлов в указанной папке с периодичностью в заданное количество минут."
PARAMS = {"source_folder": "путь к папке для резервного копирования", "backup_folder": "путь к папке резервного копирования", "interval_minutes": "интервал в минутах (по умолчанию 60)"}
DANGEROUS = False

def run(source_folder=None, backup_folder=None, interval_minutes=60):
    if not source_folder or not backup_folder:
        return "Укажи путь к папке для резервного копирования и путь к папке резервного копирования."
    
    import os
    import shutil
    import time
    import datetime
    
    try:
        interval_minutes = int(interval_minutes)
        while True:
            current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            backup_path = os.path.join(backup_folder, f"backup_{current_time}")
            shutil.make_archive(backup_path, 'zip', source_folder)
            print(f"Создан резервный архив: {backup_path}.zip")
            time.sleep(interval_minutes * 60)
    except Exception as e:
        return f"Произошла ошибка: {str(e)}"
    
    return "Резервное копирование работает."