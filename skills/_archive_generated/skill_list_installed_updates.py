NAME = "list_installed_updates"
DESCRIPTION = "Показывает информацию о установленных обновлениях Windows."
PARAMS = {}
DANGEROUS = False

def run():
    import subprocess

    try:
        # Используем WMIC для получения списка установленных обновлений
        result = subprocess.run(['wmic', 'qfe', 'list', 'brief'], capture_output=True, text=True, check=True)
        updates = result.stdout.strip()
        if not updates:
            return "Нет установленных обновлений."
        return updates
    except subprocess.CalledProcessError as e:
        return f"Ошибка при получении списка обновлений: {e.stderr}"
    except Exception as e:
        return f"Произошла ошибка: {str(e)}"