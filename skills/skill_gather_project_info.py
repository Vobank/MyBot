import os

NAME = "gather_project_info"
DESCRIPTION = "Собирает и сохраняет важную информацию о проекте в заметку."

def run(text=""):
    project_path = text.strip() or os.getcwd()
    if not os.path.isdir(project_path):
        return "Указанный путь не является директорией проекта."
    
    # Используем ранее созданные навыки для сбора информации
    git_status = show_git_status.run(project_path)
    git_log = show_git_log.run(project_path)
    installed_packages = show_installed_packages.run(project_path)
    active_processes = show_active_processes.run()
    cpu_memory_usage = show_cpu_memory_usage.run()
    
    # Формируем заметку
    note_content = f"Статус проекта: {project_path}\n\n"
    note_content += f"Git статус:\n{git_status}\n\n"
    note_content += f"Последние коммиты:\n{git_log}\n\n"
    note_content += f"Установленные пакеты:\n{installed_packages}\n\n"
    note_content += f"Активные процессы:\n{active_processes}\n\n"
    note_content += f"Использование ресурсов:\n{cpu_memory_usage}\n\n"
    
    # Сохраняем заметку
    note_filename = os.path.join(project_path, "project_info.txt")
    with open(note_filename, "w") as note_file:
        note_file.write(note_content)
    
    return f"Заметка о проекте сохранена в {note_filename}."