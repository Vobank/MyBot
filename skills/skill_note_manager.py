NAME = "note_manager"
DESCRIPTION = "Создает, редактирует и удаляет заметки в текстовом файле."
PARAMS = {
    "action": "действие (create, edit, delete, read)",
    "note_name": "название заметки",
    "note_content": "содержимое заметки (для create и edit)"
}
DANGEROUS = True   # Потому что можем удалять заметки

def run(action="read", note_name="", note_content=""):
    import os
    
    NOTES_DIR = "notes"
    os.makedirs(NOTES_DIR, exist_ok=True)
    note_path = os.path.join(NOTES_DIR, f"{note_name}.txt")

    try:
        if action == "create":
            if os.path.exists(note_path):
                return f"Заметка {note_name} уже существует."
            with open(note_path, 'w', encoding="utf-8") as f:
                f.write(note_content)
            return f"Создана заметка {note_name}."
        
        elif action == "edit":
            if not os.path.exists(note_path):
                return f"Заметка {note_name} не существует."
            with open(note_path, 'w', encoding="utf-8") as f:
                f.write(note_content)
            return f"Заметка {note_name} отредактирована."
        
        elif action == "delete":
            if not os.path.exists(note_path):
                return f"Заметка {note_name} не существует."
            os.remove(note_path)
            return f"Заметка {note_name} удалена."
        
        elif action == "read":
            if not os.path.exists(note_path):
                return f"Заметка {note_name} не существует."
            with open(note_path, 'r', encoding="utf-8") as f:
                content = f.read()
            return f"Содержимое заметки {note_name}:\n{content}"
        
        else:
            return "Неизвестное действие. Используйте create, edit, delete или read."
    
    except Exception as e:
        return f"Произошла ошибка: {str(e)}"