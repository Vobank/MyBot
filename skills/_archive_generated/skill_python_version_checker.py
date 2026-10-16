import subprocess
import re

NAME = "python_version_checker"
DESCRIPTION = "Анализирует и выводит информацию о установленных версиях Python на ПК."

def run(text=""):
    try:
        # Получаем список версий Python, используя команду в терминале
        result = subprocess.run(["py", "-0"], capture_output=True, text=True)
        output = result.stdout

        # Используем регулярное выражение для извлечения информации о версиях
        versions = re.findall(r"Python (\d+\.\d+\.\d+)", output)

        # Формируем вывод
        if versions:
            result = "Установленные версии Python:\n" + "\n".join(versions)
        else:
            result = "Не удалось найти информацию о установленных версиях Python."
    except Exception as e:
        result = f"Произошла ошибка: {str(e)}"

    return result