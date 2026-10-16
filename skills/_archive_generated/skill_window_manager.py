NAME = "window_manager"
DESCRIPTION = "Управляет окнами активного приложения (свернуть, развернуть, закрыть)."
PARAMS = {"action": "действие: minimize, maximize, close"}
DANGEROUS = True

def run(action=""):
    import subprocess

    if not action:
        return "Укажите действие: minimize, maximize или close."

    actions = {
        "minimize": "Minimize",
        "maximize": "Restore",
        "close": "Close"
    }

    if action not in actions:
        return "Неверное действие. Допустимые действия: minimize, maximize или close."

    try:
        result = subprocess.run(
            ["powershell", "-Command", f"(Get-Process -Id $pid).MainWindowHandle | Set-Window -Action {actions[action]}"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            return f"Окно активного приложения {action}ed."
        else:
            return f"Не удалось {action} окно: {result.stderr}"
    except subprocess.TimeoutExpired:
        return "Действие не завершено в течение 5 секунд."
    except Exception as e:
        return f"Произошла ошибка: {str(e)}"