NAME = "sort_files_by_extension"
DESCRIPTION = "Сортирует файлы в папке по расширению, создавая подпапки для каждого типа файлов."
PARAMS = {"path": "папка для сортировки (по умолчанию текущая)"}
DANGEROUS = True

def run(path="."):
    import os
    import shutil

    path = path or "."

    if not os.path.isdir(path):
        return "Указанный путь не является папкой."

    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    
    if not files:
        return "Нет файлов для сортировки."

    for file in files:
        _, ext = os.path.splitext(file)
        ext = ext[1:]  # remove the dot
        target_dir = os.path.join(path, ext)

        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        src_file = os.path.join(path, file)
        dst_file = os.path.join(target_dir, file)
        
        try:
            shutil.move(src_file, dst_file)
        except Exception as e:
            return f"Ошибка при перемещении файла {file}: {str(e)}"

    return "Файлы отсортированы по расширению."