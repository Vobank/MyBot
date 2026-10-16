NAME = "show_detailed_git_log"
DESCRIPTION = "Показывает историю коммитов Git с подробной информацией"

def run(text=""):
    import subprocess

    try:
        result = subprocess.run(["git", "log", "--pretty=format:%H %an %ar %s"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            return f"Ошибка: {result.stderr}"
        else:
            detailed_log = result.stdout
            return detailed_log
    except Exception as e:
        return f"Произошла ошибка: {str(e)}"