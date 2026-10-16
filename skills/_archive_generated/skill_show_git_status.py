import subprocess

NAME = "show_git_status"
DESCRIPTION = "Показывает статус текущего git-репозитория."

def run(text=""):
    try:
        result = subprocess.run(['git', 'status'], capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Ошибка при выполнении команды git status: {e.stderr}"