import os
import subprocess

NAME = "explain_git_diff_last_commit"
DESCRIPTION = "Показывает различия между текущим состоянием проекта и последним коммитом в формате объяснения изменений."

def run(text=""):
    try:
        # Получаем разницу между текущим состоянием проекта и последним коммитом
        diff_output = subprocess.check_output(["git", "diff", "HEAD"], stderr=subprocess.STDOUT).decode("utf-8")
        
        # Если нет изменений
        if not diff_output.strip():
            return "Нет изменений в проекте с момента последнего коммита."
        
        # Преобразуем diff в более понятное объяснение
        explanation = "Изменения с момента последнего коммита:\n"
        lines = diff_output.splitlines()
        for line in lines:
            if line.startswith("diff --git"):
                explanation += f"\nФайл: {line.split('b/')[1]}\n"
            elif line.startswith("-"):
                explanation += f"Удалена строка: {line[1:]}\n"
            elif line.startswith("+"):
                explanation += f"Добавлена строка: {line[1:]}\n"
        
        return explanation
    except subprocess.CalledProcessError as e:
        return f"Ошибка при попытке получить изменения: {e.output.decode('utf-8')}"
    except Exception as e:
        return f"Произошла ошибка: {str(e)}"