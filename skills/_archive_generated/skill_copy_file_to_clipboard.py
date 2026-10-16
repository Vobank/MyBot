NAME = "copy_file_to_clipboard"
DESCRIPTION = "Копирует содержимое указанного файла в буфер обмена."
PARAMS = {"path": "путь к файлу"}
DANGEROUS = False

def run(path=""):
    if not path:
        return "Укажи путь к файлу."
    
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as file:
            content = file.read()
            import pyperclip
            pyperclip.copy(content)
            return f"Содержимое файла {path} скопировано в буфер обмена."
    except FileNotFoundError:
        return f"Файл {path} не найден."
    except Exception as e:
        return f"Произошла ошибка при чтении файла: {str(e)}"