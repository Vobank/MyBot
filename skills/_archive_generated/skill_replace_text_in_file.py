NAME = "replace_text_in_file"
DESCRIPTION = "Заменяет все вхождения одного текста другим в файле."
PARAMS = {"file_path": "путь к файлу", "old_text": "текст для замены", "new_text": "новый текст"}
def run(file_path="", old_text="", new_text=""):
    if not file_path:
        return "Укажите путь к файлу."
    if not old_text or not new_text:
        return "Укажите текст для замены и новый текст."
    
    try:
        with open(file_path, 'r', encoding="utf-8", errors="ignore") as file:
            content = file.read()
        new_content = content.replace(old_text, new_text)
        
        if new_content != content:
            with open(file_path, 'w', encoding="utf-8") as file:
                file.write(new_content)
            return f"Текст '{old_text}' успешно заменен на '{new_text}'."
        else:
            return f"Текст '{old_text}' не найден в файле."
    except FileNotFoundError:
        return f"Файл по пути {file_path} не найден."
    except Exception as e:
        return f"Произошла ошибка: {e}"