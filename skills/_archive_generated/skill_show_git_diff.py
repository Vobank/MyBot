import subprocess

NAME = "show_git_diff"
DESCRIPTION = "Показывает различия между двумя версиями файлов в Git."

def run(text=""):
    args = text.split()
    if len(args) != 2:
        return "Использование: show_git_diff <commit1> <commit2>"

    commit1, commit2 = args
    try:
        result = subprocess.run(
            ["git", "diff", commit1, commit2],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Ошибка при выполнении команды: {e.stderr}"