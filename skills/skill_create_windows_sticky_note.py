NAME = "create_windows_sticky_note"
DESCRIPTION = "Создает заметку в системе заметок Windows (Sticky Notes)."
PARAMS = {"text": "текст заметки"}
DANGEROUS = False

def run(text=""):
    import subprocess

    if not text:
        return "Укажи текст заметки."
    
    try:
        # Используем команду для создания заметки в Sticky Notes
        subprocess.run(["powershell", "-Command", f"New-Item -Path 'HKCU:\\Software\\Microsoft\\Sticky Notes\\StickyNotes' -Name 'NewNote' -Value '{text}'"])
        return "Заметка успешно создана."
    except Exception as e:
        return f"Произошла ошибка: {str(e)}"