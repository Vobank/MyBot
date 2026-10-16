import subprocess

NAME = "show_git_diff_last_commit"
DESCRIPTION = "Показывает различия между текущим состоянием проекта и последним коммитом в формате diff."

def run(text=""):
    try:
        result = subprocess.run(["git", "diff", "HEAD"], capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Ошибка при выполнении команды: {e.stderr}"