NAME = "manage_environment_variables"
DESCRIPTION = "Управляет переменными окружения: добавляет, удаляет и показывает их."
PARAMS = {
    "action": "действие (add, remove, show)",
    "name": "имя переменной окружения",
    "value": "значение переменной окружения (для добавления)"
}
DANGEROUS = True

def run(action="show", name="", value=""):
    import os
    import subprocess

    try:
        if action.lower() == "add":
            if not name or not value:
                return "Укажите имя и значение переменной окружения."
            os.environ[name] = value
            # Добавляем переменную окружения на уровне системы
            subprocess.run(["setx", name, value], check=True)
            return f"Переменная окружения {name} добавлена со значением {value}."
        
        elif action.lower() == "remove":
            if not name:
                return "Укажите имя переменной окружения."
            if name in os.environ:
                del os.environ[name]
                # Удаляем переменную окружения на уровне системы
                subprocess.run(["setx", name, ""], check=True)
                return f"Переменная окружения {name} удалена."
            else:
                return f"Переменная окружения {name} не найдена."
        
        elif action.lower() == "show":
            if name:
                if name in os.environ:
                    return f"Переменная окружения {name}: {os.environ[name]}"
                else:
                    return f"Переменная окружения {name} не найдена."
            else:
                variables = "\n".join([f"{k}: {v}" for k, v in os.environ.items()])
                return variables
        else:
            return "Действие не распознано. Укажите 'add', 'remove' или 'show'."
    except Exception as e:
        return f"Ошибка: {str(e)}"