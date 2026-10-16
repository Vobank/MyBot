NAME = "folder_summary"
DESCRIPTION = "Создает краткий отчет о содержимом указанной папки, включая количество файлов, их размер и типы расширений."
PARAMS = {"path": "путь к папке (по умолчанию текущая)"}
def run(path="."):
    import os
    
    if not os.path.isdir(path):
        return "Указанный путь не является папкой."
    
    total_files = 0
    total_size = 0
    extensions = {}

    for root, _, files in os.walk(path):
        for file in files:
            total_files += 1
            filepath = os.path.join(root, file)
            try:
                total_size += os.path.getsize(filepath)
                ext = os.path.splitext(file)[1]
                if ext not in extensions:
                    extensions[ext] = 0
                extensions[ext] += 1
            except Exception as e:
                continue

    summary = f"В папке {path}:\n"
    summary += f"Количество файлов: {total_files}\n"
    summary += f"Общий размер файлов: {total_size} байт\n"
    summary += "Количество файлов по расширениям:\n"
    for ext, count in extensions.items():
        summary += f"{ext}: {count}\n"

    return summary