NAME = "manage_package_versions"
DESCRIPTION = "Управляет версиями пакетов Python в виртуальном окружении"

def run(text=""):
    import subprocess

    command_parts = text.split()
    if not command_parts:
        return "Необходимо указать пакет и желаемую версию в формате 'manage_package_versions <пакет> <версия>'"

    package = command_parts[0]
    version = command_parts[1]

    try:
        # Устанавливаем конкретную версию пакета
        result = subprocess.run(['pip', 'install', f'{package}=={version}'], capture_output=True, text=True)
        if result.returncode != 0:
            return f"Ошибка установки версии {version} пакета {package}:\n{result.stderr}"
        return f"Установлена версия {version} пакета {package}"
    except Exception as e:
        return f"Произошла ошибка: {str(e)}"