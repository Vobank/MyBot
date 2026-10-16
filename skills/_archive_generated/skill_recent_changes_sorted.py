NAME = "recent_changes_sorted"
DESCRIPTION = "Показывает последние изменения в файлах папки, отсортированные по времени изменения."
PARAMS = {"path": "папка (по умолчанию текущая)"}
DANGEROUS = False

def run(path="."):
    import os
    from datetime import datetime

    if not os.path.exists(path):
        return f"Папка {path} не существует."

    # Получаем список файлов и директорий
    items = [(os.path.join(path, f), os.path.getmtime(os.path.join(path, f))) for f in os.listdir(path)]
    items = [(f, datetime.fromtimestamp(mtime)) for f, mtime in items if os.path.isfile(f)]

    # Сортируем по времени изменения
    items.sort(key=lambda item: item[1], reverse=True)

    # Формируем результат
    result = []
    for f, mtime in items[:100]:  # Ограничиваем результат 100 файлами
        result.append(f"{mtime.strftime('%Y-%m-%d %H:%M:%S')} - {os.path.basename(f)}")
    
    return "\n".join(result) if result else "Нет изменений."