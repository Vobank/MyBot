NAME = "task_manager"
DESCRIPTION = "Управляет списком задач пользователя (добавление, удаление, просмотр)."
PARAMS = {"action": "действие (add, delete, list)", "task": "текст задачи (для add и delete)"}
DANGEROUS = False

def run(action="list", task=""):
    import os

    tasks_file = "tasks.txt"
    
    if not os.path.exists(tasks_file):
        open(tasks_file, "w").close()

    if action == "add":
        if not task:
            return "Укажи текст задачи для добавления."
        with open(tasks_file, "a") as f:
            f.write(task + "\n")
        return f"Задача '{task}' добавлена."
    
    elif action == "delete":
        if not task:
            return "Укажи текст задачи для удаления."
        try:
            with open(tasks_file, "r") as f:
                lines = f.readlines()
            with open(tasks_file, "w") as f:
                deleted = False
                for line in lines:
                    if line.strip() != task:
                        f.write(line)
                    else:
                        deleted = True
                if deleted:
                    return f"Задача '{task}' удалена."
                else:
                    return f"Задача '{task}' не найдена."
        except Exception as e:
            return str(e)
    
    elif action == "list":
        try:
            with open(tasks_file, "r") as f:
                tasks = f.readlines()
            if tasks:
                return "\n".join([f"{i+1}. {task.strip()}" for i, task in enumerate(tasks)])
            else:
                return "Список задач пуст."
        except Exception as e:
            return str(e)
    
    else:
        return "Неправильное действие. Используй 'add', 'delete' или 'list'."