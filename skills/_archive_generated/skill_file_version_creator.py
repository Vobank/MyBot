NAME = "file_version_creator"
DESCRIPTION = "Создает версионированные копии файла в указанной папке."
PARAMS = {"file_path": "путь к файлу", "folder_path": "папка для сохранения версий"}
DANGEROUS = False

def run(file_path="", folder_path="."):
    import os
    import shutil
    from datetime import datetime

    if not file_path:
        return "Укажи путь к файлу."

    if not os.path.exists(file_path):
        return f"Файл {file_path} не найден."

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    versioned_filename = f"{os.path.basename(file_path)}_{timestamp}"
    versioned_file_path = os.path.join(folder_path, versioned_filename)

    try:
        shutil.copy2(file_path, versioned_file_path)
        return f"Версионированная копия файла {file_path} создана: {versioned_file_path}"
    except Exception as e:
        return f"Ошибка при создании версионированной копии: {str(e)}"