NAME = "recent_changes_report"
DESCRIPTION = "Создает отчет о недавно измененных файлах в указанной папке."
PARAMS = {"path": "папка (по умолчанию текущая)", "days": "количество дней (по умолчанию 7)"}
DANGEROUS = False

def run(path=".", days=7):
    import os
    import time

    if not os.path.isdir(path):
        return "Указанная папка не существует."
    
    cutoff_time = time.time() - (days * 24 * 60 * 60)
    recent_files = []
    
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            mod_time = os.path.getmtime(file_path)
            if mod_time > cutoff_time:
                recent_files.append(f"{file_path} - {time.ctime(mod_time)}")
    
    if recent_files:
        return "\n".join(recent_files)
    else:
        return "Нет измененных файлов за последние {days} дней.".format(days=days)