NAME = "show_file_content"
DESCRIPTION = "Показывает содержимое указанного файла."
PARAMS = {"file_path": "путь к файлу"}
DANGEROUS = False

def run(file_path=""):
    if not file_path:
        return "Укажи путь к файлу."

    try:
        with open(file_path, encoding="utf-8", errors="ignore") as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return f"Файл по пути {file_path} не найден."
    except Exception as e:
        return f"Ошибка при чтении файла: {e}"