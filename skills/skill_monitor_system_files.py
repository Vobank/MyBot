NAME = "monitor_system_files"
DESCRIPTION = "Отслеживает изменения в системных файлах и предупреждает о необычных изменениях."
PARAMS = {"path": "путь к системной папке для мониторинга (по умолчанию C:\\Windows)"}
DANGEROUS = False

def run(path="C:\\Windows"):
    import os
    import hashlib
    import time

    # Функция для вычисления контрольной суммы файла
    def get_hash(filename):
        try:
            with open(filename, 'rb') as f:
                return hashlib.sha256(f.read()).hexdigest()
        except Exception as e:
            return str(e)

    # Словарь для хранения контрольных сумм файлов
    file_hashes = {}

    # Получение контрольных сумм файлов
    for root, _, files in os.walk(path):
        for file in files:
            filepath = os.path.join(root, file)
            file_hashes[filepath] = get_hash(filepath)

    # Ждем некоторое время
    time.sleep(30)  # Пауза в 30 секунд

    # Повторное получение контрольных сумм и сравнение с предыдущими
    changes = []
    for root, _, files in os.walk(path):
        for file in files:
            filepath = os.path.join(root, file)
            new_hash = get_hash(filepath)
            if file_hashes.get(filepath) != new_hash:
                changes.append(f"Изменение в файле: {filepath}")

    return "\n".join(changes) if changes else "Нет изменений в системных файлах."