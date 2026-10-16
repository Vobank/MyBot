NAME = "mirror_text"
DESCRIPTION = "Преобразует текст в зеркальное отображение."
def run(text=""):
    mirrored_text = text[::-1]
    return mirrored_text