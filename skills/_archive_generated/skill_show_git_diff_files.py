import subprocess

NAME = "show_git_diff_files"
DESCRIPTION = "Показывает различия между двумя версиями файлов в проекте с использованием git."

def run(text=""):
    try:
        # Разбиваем входной текст на части
        parts = text.split()
        if len(parts) != 3:
            return "Неверный формат ввода. Используйте: show_git_diff_files <файл> <коммит1> <коммит2>"
        
        file_path, commit1, commit2 = parts
        # Получаем различия между двумя версиями файла в проекте с использованием git
        diff = subprocess.check_output(f"git diff {commit1} {commit2} -- {file_path}", shell=True, stderr=subprocess.STDOUT).decode()
        return diff
    except subprocess.CalledProcessError as e:
        return f"Произошла ошибка при выполнении команды: {e.output.decode()}"