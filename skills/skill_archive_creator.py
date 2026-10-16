NAME = "archive_creator"
DESCRIPTION = "Создает архив всех файлов в указанной папке с возможностью добавления описания в архив."
PARAMS = {
    "path": "путь к папке",
    "description": "описание архива (по умолчанию пустое)"
}
DANGEROUS = False

def run(path=".", description=""):
    import os
    import zipfile

    if not os.path.isdir(path):
        return f"Папка {path} не найдена."

    archive_name = f"{os.path.basename(path)}_{os.path.getctime(path)}.zip"
    archive_path = os.path.join(os.path.dirname(path), archive_name)

    with zipfile.ZipFile(archive_path, 'w') as zipf:
        for root, _, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, path))
        if description:
            description_path = os.path.join(path, "description.txt")
            with open(description_path, 'w') as desc_file:
                desc_file.write(description)
            zipf.write(description_path, os.path.relpath(description_path, path))
            os.remove(description_path)

    return f"Архив создан: {archive_path}"