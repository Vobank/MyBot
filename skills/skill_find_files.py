import os
import fnmatch

NAME = "find_files"
DESCRIPTION = "Ищет файлы по шаблону в указанной директории."

def run(directory=".", pattern="*"):
    try:
        found_files = []
        for root, dirs, files in os.walk(directory):
            for base_name in files:
                if fnmatch.fnmatch(base_name, pattern):
                    found_files.append(os.path.join(root, base_name))
        return "\n".join(found_files) if found_files else "Ничего не найдено."
    except Exception as e:
        return f"Произошла ошибка: {str(e)}"