import subprocess

NAME = "git_create_backup"
DESCRIPTION = "Создает резервную копию указанного проекта с использованием git."

def run(text=""):
    project_path = text.strip()
    try:
        # Проверка наличия git в проекте
        subprocess.run(["git", "rev-parse"], check=True, cwd=project_path)

        # Создание резервной копии
        backup_name = f"backup-{project_path.split('/')[-1]}"
        subprocess.run(["git", "clone", project_path, backup_name], check=True)
        return f"Резервная копия проекта создана в {backup_name}."
    except subprocess.CalledProcessError as e:
        return f"Ошибка при создании резервной копии: {e}"