NAME = "image_operations"
DESCRIPTION = "Выполняет базовые операции с изображениями: изменение размера, конвертирование формата."
PARAMS = {
    "image_path": "путь к изображению",
    "operation": "операция (resize, convert)",
    "new_size": "новый размер изображения (ширинаxвысота, например, 800x600)",
    "new_format": "новый формат изображения (например, jpg, png)"
}
DANGEROUS = False

def run(image_path="", operation="", new_size="", new_format=""):
    from PIL import Image
    import os

    if not image_path:
        return "Укажите путь к изображению."
    if not operation or operation not in ["resize", "convert"]:
        return "Укажите операцию (resize или convert)."
    if operation == "resize" and not new_size:
        return "Укажите новый размер изображения (например, 800x600)."
    if operation == "convert" and not new_format:
        return "Укажите новый формат изображения (например, jpg)."

    try:
        img = Image.open(image_path)
        base_path, ext = os.path.splitext(image_path)

        if operation == "resize":
            width, height = map(int, new_size.split('x'))
            img = img.resize((width, height), Image.ANTIALIAS)
            new_path = f"{base_path}_resized{ext}"
        elif operation == "convert":
            new_path = f"{base_path}.{new_format}"

        img.save(new_path)
        return f"Изображение успешно обработано и сохранено по пути {new_path}."
    except Exception as e:
        return f"Произошла ошибка при обработке изображения: {str(e)}"