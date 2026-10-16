NAME = "get_pixel_color"
DESCRIPTION = "Считывает цвет пикселя на экране по указанным координатам."
PARAMS = {"x": "координата X", "y": "координата Y"}
DANGEROUS = False

def run(x=0, y=0):
    try:
        from PIL import ImageGrab
        screenshot = ImageGrab.grab()
        pixel_color = screenshot.getpixel((int(x), int(y)))
        return f"Цвет пикселя по координатам ({x}, {y}): RGB {pixel_color}"
    except ValueError:
        return "Координаты должны быть целыми числами."
    except Exception as e:
        return f"Произошла ошибка: {str(e)}"