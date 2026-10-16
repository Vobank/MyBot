NAME = "installed_programs_info"
DESCRIPTION = "Показывает информацию о установленных программах и их версиях."
PARAMS = {"software_name": "имя программы (по умолчанию показывает все)"}
DANGEROUS = False

def run(software_name=""):
    import subprocess

    try:
        # Получаем список установленных программ
        result = subprocess.run(["wmic", "product", "get", "name,version"], capture_output=True, text=True)
        output = result.stdout.strip()

        # Фильтруем результат по имени программы, если оно указано
        if software_name:
            lines = output.split("\n")
            filtered_output = [line for line in lines if software_name.lower() in line.lower()]
            output = "\n".join(filtered_output)

        return output if output else "Нет установленных программ или не найдено совпадений."
    except Exception as e:
        return f"Произошла ошибка: {str(e)}"