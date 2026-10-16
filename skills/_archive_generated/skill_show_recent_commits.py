import subprocess

NAME = "show_recent_commits"
DESCRIPTION = "Показывает последние коммиты в репозитории с возможностью указать количество коммитов."

def run(text=""):
    try:
        if text:
            count = int(text)
        else:
            count = 5  # default number of commits to show

        result = subprocess.run(['git', 'log', '-n', str(count), '--pretty=format:%h %s'], capture_output=True, text=True, check=True)
        commits = result.stdout.strip().split('\n')
        return '\n'.join(commits)
    except subprocess.CalledProcessError as e:
        return f"Ошибка при выполнении команды: {e.stderr.strip()}"
    except Exception as e:
        return f"Произошла ошибка: {str(e)}"