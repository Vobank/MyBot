NAME = "analyze_system_logs"
DESCRIPTION = "Анализирует системные журналы и выделяет важные события или ошибки."
PARAMS = {"log_path": "путь к журналу (по умолчанию использует логи системы)"}
DANGEROUS = False

def run(log_path=""):
    import os
    import re

    if not log_path:
        log_path = "C:\\Windows\\System32\\winevt\\Logs\\Application.evtx"
        return "Укажите путь к журналу или используйте стандартный путь для журналов системы."

    try:
        # Пример обработки текстового файла с логами. Для работы с EVTX файлами потребуется сторонняя библиотека.
        with open(log_path, "r", encoding="utf-8", errors="ignore") as log_file:
            log_content = log_file.read()
        
        # Ищем ошибки и предупреждения
        errors = re.findall(r"ERROR|WARNING", log_content)
        error_count = len(errors)
        
        if error_count == 0:
            return "В журнале не найдено ошибок или предупреждений."
        else:
            return f"Найдено {error_count} ошибок или предупреждений.\nПримеры:\n{errors[:10]}"
    except FileNotFoundError:
        return f"Файл по пути {log_path} не найден."
    except Exception as e:
        return f"Произошла ошибка при обработке журнала: {str(e)}"