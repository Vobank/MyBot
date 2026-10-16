NAME = "group_files_by_extension"
DESCRIPTION = "Группирует файлы в указанной папке по расширению, перемещая их в соответствующие подпапки."
PARAMS = {"path": "папка для анализа и группировки файлов"}
DANGEROUS = True

import os
import shutil

def run(path="."):
    if not os.path.isdir(path):
        return f"Указанный путь '{path}' не является папкой."

    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    if not files:
        return "Нет файлов для группировки."

    for file in files:
        file_path = os.path.join(path, file)
        file_extension = os.path.splitext(file)[1].lstrip('.')
        if file_extension:
            extension_folder = os.path.join(path, file_extension)
            if not os.path.exists(extension_folder):
                os.makedirs(extension_folder)
            shutil.move(file_path, os.path.join(extension_folder, file))

    return f"Файлы успешно группированы по расширению в папке '{path}'."