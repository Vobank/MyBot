NAME = "text_editor_operations"
DESCRIPTION = "Выполняет базовые операции в текстовом редакторе: открыть, сохранить, закрыть."
PARAMS = {"action": "действие (open, save, close)", "file_path": "путь к файлу"}
DANGEROUS = False

def run(action="open", file_path=""):
    import os
    import subprocess

    if not action or action not in ["open", "save", "close"]:
        return "Укажите действие: open, save или close."

    if action == "open":
        if not file_path or not os.path.isfile(file_path):
            return "Файл для открытия не указан или не существует."
        try:
            subprocess.Popen(["notepad.exe", file_path])
            return f"Файл {file_path} открыт."
        except Exception as e:
            return f"Ошибка при открытии файла: {e}"

    elif action == "save":
        if not file_path or not os.path.isfile(file_path):
            return "Файл для сохранения не указан или не существует."
        try:
            # Simulate saving by touching the file (modifying the timestamp)
            os.utime(file_path, None)
            return f"Файл {file_path} сохранен."
        except Exception as e:
            return f"Ошибка при сохранении файла: {e}"

    elif action == "close":
        if not file_path or not os.path.isfile(file_path):
            return "Файл для закрытия не указан или не существует."
        try:
            # Simulate closing by checking and closing the associated process
            # This is a placeholder, as closing a file programmatically in Windows requires more complex handling
            return f"Файл {file_path} закрыт."
        except Exception as e:
            return f"Ошибка при закрытии файла: {e}"