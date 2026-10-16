NAME = "clipboard_manager"
DESCRIPTION = "Управляет буфером обмена: считывает содержимое буфера, копирует текст в буфер и очищает буфер."
PARAMS = {"action": "действие (read, write, clear)", "text": "текст для записи в буфер (если нужно)"}
DANGEROUS = False

def run(action="read", text=""):
    import tkinter as tk

    def read_clipboard():
        root = tk.Tk()
        root.withdraw()
        clipboard_content = root.clipboard_get()
        root.destroy()
        return clipboard_content

    def write_clipboard(text):
        root = tk.Tk()
        root.withdraw()
        root.clipboard_clear()
        root.clipboard_append(text)
        root.destroy()
        return f"Текст '{text[:50]}' записан в буфер обмена."

    def clear_clipboard():
        root = tk.Tk()
        root.withdraw()
        root.clipboard_clear()
        root.destroy()
        return "Буфер обмена очищен."

    try:
        if action == "read":
            return read_clipboard()
        elif action == "write":
            if not text:
                return "Укажите текст для записи в буфер."
            return write_clipboard(text)
        elif action == "clear":
            return clear_clipboard()
        else:
            return "Неверное действие. Допустимые значения: read, write, clear."
    except Exception as e:
        return f"Произошла ошибка: {str(e)}"