NAME = "manage_file_timestamps"
DESCRIPTION = "Управляет временными метками файлов: изменение даты создания, модификации и последнего доступа."
PARAMS = {
    "path": "путь к файлу",
    "created": "новая дата создания (в формате YYYY-MM-DD HH:MM:SS)",
    "modified": "новая дата модификации (в формате YYYY-MM-DD HH:MM:SS)",
    "accessed": "новая дата последнего доступа (в формате YYYY-MM-DD HH:MM:SS)"
}
DANGEROUS = True

def run(path="", created=None, modified=None, accessed=None):
    import os
    import time
    from datetime import datetime

    if not path:
        return "Укажи путь к файлу."
    
    if not os.path.exists(path):
        return "Файл не существует."
    
    if not any([created, modified, accessed]):
        return "Укажи хотя бы одну дату для изменения (created, modified, accessed)."
    
    try:
        ctime = datetime.strptime(created, "%Y-%m-%d %H:%M:%S").timestamp() if created else None
        mtime = datetime.strptime(modified, "%Y-%m-%d %H:%M:%S").timestamp() if modified else None
        atime = datetime.strptime(accessed, "%Y-%m-%d %H:%M:%S").timestamp() if accessed else None
        
        if ctime is not None:
            os.utime(path, times=(atime or os.path.getatime(path), mtime or os.path.getmtime(path)))
        else:
            os.utime(path, times=(atime or os.path.getatime(path), mtime or os.path.getmtime(path)))
        
        return "Временные метки успешно изменены."
    except ValueError:
        return "Неверный формат даты. Используй формат YYYY-MM-DD HH:MM:SS."
    except Exception as e:
        return f"Ошибка при изменении меток времени: {str(e)}"