NAME = "monitor_file_changes"
DESCRIPTION = "Мониторит изменения в файлах папки и оповещает о них."
PARAMS = {"path": "путь к папке для мониторинга", "interval": "интервал проверки (в секундах)"}
DANGEROUS = False

def run(path=".", interval=60):
    import os
    import time
    from collections import defaultdict

    # Сохраняем текущие метаданные файлов
    file_data = defaultdict(dict)
    for root, _, files in os.walk(path):
        for filename in files:
            filepath = os.path.join(root, filename)
            try:
                file_data[filepath]["timestamp"] = os.path.getmtime(filepath)
                file_data[filepath]["size"] = os.path.getsize(filepath)
            except Exception as e:
                return f"Ошибка чтения файла {filepath}: {e}"
    
    time.sleep(interval)
    
    # Проверяем изменения
    changes_detected = False
    result = []
    for root, _, files in os.walk(path):
        for filename in files:
            filepath = os.path.join(root, filename)
            try:
                current_timestamp = os.path.getmtime(filepath)
                current_size = os.path.getsize(filepath)
                if filepath not in file_data:
                    changes_detected = True
                    result.append(f"Новый файл: {filepath}")
                elif current_timestamp != file_data[filepath]["timestamp"] or current_size != file_data[filepath]["size"]:
                    changes_detected = True
                    result.append(f"Изменения в файле: {filepath} (дата изменения: {current_timestamp}, размер: {current_size})")
            except Exception as e:
                result.append(f"Ошибка чтения файла {filepath}: {e}")
    
    if not changes_detected:
        result.append("Нет изменений.")
    
    return "\n".join(result)