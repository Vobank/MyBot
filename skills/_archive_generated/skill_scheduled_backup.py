NAME = "scheduled_backup"
DESCRIPTION = "Создает автоматические резервные копии файлов по заданному расписанию."
PARAMS = {"pattern": "шаблон для файлов", "path": "путь к папке", "schedule": "расписание"}
DANGEROUS = True

def run(pattern="*.py", path=".", schedule="daily"):
    import os
    import shutil
    import time
    import datetime
    
    if not pattern or not path or not schedule:
        return "Укажи шаблон для файлов, путь к папке и расписание."
    
    try:
        while True:
            now = datetime.datetime.now()
            if schedule == "daily":
                if now.hour == 0 and now.minute == 0:
                    for root, _, files in os.walk(path):
                        for fn in files:
                            if fn.endswith(pattern):
                                src = os.path.join(root, fn)
                                dst = os.path.join(path, "backups", f"{fn}_{now.strftime('%Y%m%d_%H%M%S')}")
                                os.makedirs(os.path.dirname(dst), exist_ok=True)
                                shutil.copy2(src, dst)
                                print(f"Создана резервная копия: {dst}")
                    time.sleep(3600)  # ждем час
            elif schedule == "weekly":
                if now.weekday() == 0 and now.hour == 0 and now.minute == 0:
                    for root, _, files in os.walk(path):
                        for fn in files:
                            if fn.endswith(pattern):
                                src = os.path.join(root, fn)
                                dst = os.path.join(path, "backups", f"{fn}_{now.strftime('%Y%m%d_%H%M%S')}")
                                os.makedirs(os.path.dirname(dst), exist_ok=True)
                                shutil.copy2(src, dst)
                                print(f"Создана резервная копия: {dst}")
                    time.sleep(86400 * 7)  # ждем неделю
            else:
                return "Неподдерживаемое расписание."
    except Exception as e:
        return f"Произошла ошибка: {str(e)}"
    
    return "Резервное копирование завершено."