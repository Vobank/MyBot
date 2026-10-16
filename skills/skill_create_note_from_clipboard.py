import tkinter
import os

NAME = "create_note_from_clipboard"
DESCRIPTION = "Создает заметку из текста в буфере обмена"

def run(text=""):
    # Инициализируем Tkinter для доступа к буферу обмена
    root = tkinter.Tk()
    root.withdraw()  # Скрываем основное окно Tkinter
    clipboard_text = root.clipboard_get()  # Получаем текст из буфера обмена
    
    if not clipboard_text:
        return "Буфер обмена пуст."
    
    # Определяем путь к папке для заметок
    notes_dir = os.path.expanduser("~/notes")
    if not os.path.exists(notes_dir):
        os.makedirs(notes_dir)
    
    # Генерируем имя файла для заметки
    note_file = os.path.join(notes_dir, f"note_{len(os.listdir(notes_dir)) + 1}.txt")
    
    # Записываем текст в файл
    with open(note_file, "w") as f:
        f.write(clipboard_text)
    
    return f"Заметка создана: {note_file}"