import subprocess

NAME = "git_branch_management"
DESCRIPTION = "Управление ветками git: создание, переключение, удаление."

def run(action, branch_name=""):
    actions = {
        "create": f"git branch {branch_name}",
        "switch": f"git checkout {branch_name}",
        "delete": f"git branch -d {branch_name}",
    }

    if action not in actions:
        return "Неверное действие. Допустимые действия: create, switch, delete."

    try:
        result = subprocess.run(actions[action], shell=True, check=True, capture_output=True, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return e.stderr