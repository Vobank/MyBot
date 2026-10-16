NAME = "sort_files_by_extension"
DESCRIPTION = "Сортирует файлы в папке по их расширениям, перемещая их в соответствующие подпапки."
PARAMS = {"path": "папка, где нужно отсортировать файлы"}
DANGEROUS = True

def run(path="."):
    import os
    import shutil

    if not os.path.isdir(path):
        return "Указанная папка не существует."

    files = os.listdir(path)
    moved_files = []

    for filename in files:
        file_path = os.path.join(path, filename)
        if os.path.isfile(file_path):
            extension = filename.rsplit('.', 1)[-1].lower()
            target_dir = os.path.join(path, extension)

            if not os.path.exists(target_dir):
                os.makedirs(target_dir)

            shutil.move(file_path, os.path.join(target_dir, filename))
            moved_files.append(filename)

    if moved_files:
        return f"Перемещены файлы: {', '.join(moved_files)}"
    else:
        return "Нет файлов для сортировки."