import os

NAME = "terminal_history_manager"
DESCRIPTION = "управлять и просматривать историю команд в терминале"

def run(action="view"):
    history_file = os.path.expanduser("~/.bash_history")
    if action == "view":
        with open(history_file, "r") as f:
            history = f.readlines()
        return "История команд:\n" + "\n".join(history)
    elif action == "clear":
        with open(history_file, "w"):
            pass
        return "История команд очищена."
    else:
        return "Действие не распознано. Доступные действия: view, clear"