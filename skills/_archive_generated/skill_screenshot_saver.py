NAME = "screenshot_saver"
DESCRIPTION = "Создает снимок экрана и сохраняет его в указанной папке."
PARAMS = {"path": "папка для сохранения скриншота (по умолчанию текущая)"}
DANGEROUS = False

def run(path="."):
    try:
        import os
        from PIL import ImageGrab

        if not os.path.exists(path):
            os.makedirs(path)
        
        screenshot = ImageGrab.grab()
        screenshot_file = os.path.join(path, f"screenshot_{int(time.time())}.png")
        screenshot.save(screenshot_file)
        return f"Скриншот успешно сохранен в файл: {screenshot_file}"
    except Exception as e:
        return f"Ошибка при создании скриншота: {str(e)}"