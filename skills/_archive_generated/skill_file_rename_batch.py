NAME = "file_rename_batch"
DESCRIPTION = "Массово переименовывает файлы в указанной папке по заданному шаблону."
PARAMS = {"path": "папка с файлами", "old_pattern": "старый шаблон для поиска", "new_pattern": "новый шаблон для замены"}
DANGEROUS = True  # Переименование файлов может привести к потере доступности файлов по старым путям.

def run(path=".", old_pattern="", new_pattern=""):
    import os
    if not old_pattern or not new_pattern:
        return "Укажи оба шаблона: старый и новый."
    
    if not os.path.isdir(path):
        return f"Путь '{path}' не является директорией."
    
    renamed_files = []
    for filename in os.listdir(path):
        if old_pattern in filename:
            new_filename = filename.replace(old_pattern, new_pattern)
            old_filepath = os.path.join(path, filename)
            new_filepath = os.path.join(path, new_filename)
            try:
                os.rename(old_filepath, new_filepath)
                renamed_files.append(f"{filename} -> {new_filename}")
            except Exception as e:
                return f"Ошибка при переименовании файла '{filename}': {str(e)}"
    
    if renamed_files:
        return "\n".join(renamed_files)
    else:
        return "Ничего не переименовано."