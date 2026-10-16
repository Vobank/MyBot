NAME = "sticky_notes_manager"
DESCRIPTION = "Управляет заметками в системе заметок Windows (Sticky Notes): добавляет, удаляет и показывает список заметок."
PARAMS = {"action": "действие (add, delete, list)", "note": "содержимое заметки (только для добавления)"}
DANGEROUS = False

def run(action="list", note=""):
    import subprocess
    result = ""
    
    if action.lower() == "add":
        if not note:
            return "Укажи содержимое заметки для добавления."
        try:
            subprocess.run(["StickyNotes.exe", "/add", note], check=True)
            result = f"Заметка '{note}' добавлена."
        except Exception as e:
            result = f"Ошибка при добавлении заметки: {e}"
    elif action.lower() == "delete":
        try:
            subprocess.run(["StickyNotes.exe", "/clear"], check=True)
            result = "Все заметки удалены."
        except Exception as e:
            result = f"Ошибка при удалении заметок: {e}"
    elif action.lower() == "list":
        try:
            output = subprocess.check_output(["StickyNotes.exe", "/list"], universal_newlines=True)
            result = output.strip() if output else "Нет заметок."
        except Exception as e:
            result = f"Ошибка при получении списка заметок: {e}"
    else:
        result = "Неверное действие. Используй add, delete или list."
    
    return result