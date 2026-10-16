import subprocess

NAME = "show_git_changes"
DESCRIPTION = "Показывает изменения в рабочем каталоге с помощью git."

def run(text=""):
    try:
        result = subprocess.run(["git", "status", "-s"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            return result.stdout
        else:
            return f"Ошибка при выполнении команды git status: {result.stderr}"
    except Exception as e:
        return f"Произошла ошибка: {str(e)}"