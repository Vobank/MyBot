import subprocess

NAME = "show_git_log"
DESCRIPTION = "Показывает историю коммитов в git."

def run(text=""):
    try:
        result = subprocess.run(['git', 'log', '--oneline'], capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Ошибка при выполнении команды: {e.stderr}"