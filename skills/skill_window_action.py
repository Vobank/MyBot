NAME = "window_action"
DESCRIPTION = "Выполняет действия с окнами: перемещение, изменение размера, сворачивание и разворачивание."
PARAMS = {"action": "действие с окном (move, resize, minimize, maximize)", "window_title": "название окна", "x": "координата X (только для move и resize)", "y": "координата Y (только для move и resize)", "width": "ширина (только для resize)", "height": "высота (только для resize)"}
DANGEROUS = False

def run(action="", window_title="", x=0, y=0, width=0, height=0):
    import subprocess
    import re

    if not action or not window_title:
        return "Укажи действие и название окна."

    action = action.lower()
    valid_actions = ["move", "resize", "minimize", "maximize"]
    if action not in valid_actions:
        return "Действие не поддерживается. Доступные действия: move, resize, minimize, maximize."

    # Ищем окно по названию
    window_id = None
    result = subprocess.run(["powershell", "-Command", "(Get-Process | Where-Object { $_.MainWindowTitle -like '*{}*' }).Id".format(window_title)], capture_output=True, text=True)
    if result.stdout:
        window_id = result.stdout.strip()
    else:
        return f"Окно с названием '{window_title}' не найдено."

    # Выполняем действие
    if action == "move":
        subprocess.run(["powershell", "-Command", f"(Get-Process -Id {window_id}).MainWindowTopMost = $true; (Get-Process -Id {window_id}).MainWindowTop = {y}; (Get-Process -Id {window_id}).MainWindowLeft = {x}"])
    elif action == "resize":
        subprocess.run(["powershell", "-Command", f"(Get-Process -Id {window_id}).MainWindowTopMost = $true; (Get-Process -Id {window_id}).MainWindowWidth = {width}; (Get-Process -Id {window_id}).MainWindowHeight = {height}"])
    elif action == "minimize":
        subprocess.run(["powershell", "-Command", f"(Get-Process -Id {window_id}).MainWindowTopMost = $true; (Get-Process -Id {window_id}).MainWindowState = 'Minimized'"])
    elif action == "maximize":
        subprocess.run(["powershell", "-Command", f"(Get-Process -Id {window_id}).MainWindowTopMost = $true; (Get-Process -Id {window_id}).MainWindowState = 'Maximized'"])

    return f"Действие '{action}' выполнено для окна '{window_title}'."