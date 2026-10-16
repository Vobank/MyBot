NAME = "folder_manager"
DESCRIPTION = "Управляет папками: создает, удаляет и переименовывает их."
PARAMS = {
    "action": "действие (create/delete/rename)",
    "path": "путь к папке или исходному имени при переименовании",
    "new_path": "новое имя при переименовании"
}
DANGEROUS = True

def run(action="create", path="", new_path=""):
    import os
    import shutil

    if not action or not path:
        return "Укажи действие и путь к папке."

    result = ""
    try:
        if action == "create":
            if not os.path.exists(path):
                os.makedirs(path)
                result = f"Папка '{path}' создана."
            else:
                result = f"Папка '{path}' уже существует."
        elif action == "delete":
            if os.path.exists(path):
                shutil.rmtree(path)
                result = f"Папка '{path}' удалена."
            else:
                result = f"Папка '{path}' не существует."
        elif action == "rename":
            if not new_path:
                return "Укажи новое имя при переименовании."
            if os.path.exists(path):
                shutil.move(path, new_path)
                result = f"Папка '{path}' переименована в '{new_path}'."
            else:
                result = f"Папка '{path}' не существует."
        else:
            result = "Недопустимое действие. Используй create, delete или rename."
    except Exception as e:
        result = f"Ошибка: {str(e)}"
    
    return result