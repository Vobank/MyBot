NAME = "show_detailed_git_diff_last_commit"
DESCRIPTION = "Показывает подробные различия между текущим состоянием проекта и последним коммитом."

import subprocess

def run(text=""):
    try:
        result = subprocess.run(['git', 'diff', 'HEAD'], capture_output=True, text=True, check=True)
        detailed_diff = result.stdout
        if detailed_diff:
            return detailed_diff
        else:
            return "Нет изменений по сравнению с последним коммитом."
    except subprocess.CalledProcessError as e:
        return f"Ошибка при выполнении команды git diff: {e.stderr}"