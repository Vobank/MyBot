import subprocess
import os

NAME = "auto_commit_changes"
DESCRIPTION = "Отслеживает изменения в проекте и автоматически создает коммиты"

def run(text=""):
    repo_path = text.strip() if text else os.getcwd()
    if not os.path.isdir(os.path.join(repo_path, '.git')):
        return "Указанная директория не является Git-репозиторием"

    try:
        # Проверка изменений
        diff_output = subprocess.check_output(['git', 'diff'], cwd=repo_path).decode('utf-8')
        if diff_output:
            # Создание коммита
            commit_message = "Автоматический коммит изменений"
            subprocess.run(['git', 'add', '.'], cwd=repo_path, check=True)
            commit_result = subprocess.run(['git', 'commit', '-m', commit_message], cwd=repo_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return commit_result.stdout.decode('utf-8')
        else:
            return "Нет изменений для коммита"
    except subprocess.CalledProcessError as e:
        return f"Ошибка при работе с Git: {e.stderr.decode('utf-8')}"