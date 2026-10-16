NAME = "git_file_history"
DESCRIPTION = "Показывает историю изменений git по конкретному файлу."
PARAMS = {"file_path": "путь к файлу"}
DANGEROUS = False

def run(file_path=""):
    import subprocess

    if not file_path:
        return "Укажи путь к файлу."

    try:
        result = subprocess.run(["git", "log", "--follow", "--", file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        if result.stdout:
            return result.stdout
        else:
            return "Нет истории изменений для данного файла."
    except subprocess.CalledProcessError as e:
        if "invalid reference" in e.stderr:
            return "Файл не найден в репозитории."
        elif "not a git repository" in e.stderr:
            return "Текущая директория не является репозиторием git."
        else:
            return f"Ошибка: {e.stderr}"
    except Exception as e:
        return f"Произошла ошибка: {str(e)}"