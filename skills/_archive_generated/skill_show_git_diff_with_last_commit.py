import subprocess

NAME = "show_git_diff_with_last_commit"
DESCRIPTION = "Показывает отличия между текущим состоянием проекта и предыдущим коммитом в формате диффа."

def run(text=""):
    try:
        # Получаем различия между текущим состоянием и предыдущим коммитом
        result = subprocess.run(["git", "diff", "HEAD"], capture_output=True, text=True, check=True)
        diff = result.stdout
        if diff:
            return "Отличия между текущим состоянием и предыдущим коммитом:\n" + diff
        else:
            return "Нет отличий между текущим состоянием и предыдущим коммитом."
    except subprocess.CalledProcessError as e:
        return f"Произошла ошибка при выполнении команды: {e.stderr}"