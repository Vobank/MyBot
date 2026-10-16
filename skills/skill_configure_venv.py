import os
import json

NAME = "configure_venv"
DESCRIPTION = "Автоматически создает и управляет конфигурационными файлами для виртуальных окружений."

def run(text=""):
    venv_path = text.strip()
    config_path = os.path.join(venv_path, "config.json")
    
    if not os.path.exists(venv_path):
        return f"Виртуальное окружение по пути {venv_path} не существует."
    
    if not os.path.exists(config_path):
        # Создание нового конфигурационного файла
        config = {
            "packages": [],
            "version": "0.1"
        }
        with open(config_path, 'w') as config_file:
            json.dump(config, config_file, indent=4)
        return f"Конфигурационный файл создан для виртуального окружения {venv_path}."
    
    # Чтение и обновление конфигурационного файла
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)
    
    # Пример обновления конфигурационного файла (можно добавить логику по управлению пакетами)
    if "packages" in config:
        config["packages"].append("example_package")
        with open(config_path, 'w') as config_file:
            json.dump(config, config_file, indent=4)
        return f"Конфигурационный файл обновлен для виртуального окружения {venv_path}."
    else:
        return f"Ошибка: неверный формат конфигурационного файла в {venv_path}."