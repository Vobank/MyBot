import subprocess
import os

NAME = "auto_run_script"
DESCRIPTION = "Автоматически запускает заданный скрипт Python в виртуальном окружении."

def run(text=""):
    if not text:
        return "Необходимо указать путь к скрипту Python для запуска."
    
    script_path = text.strip()
    venv_path = os.getenv('VIRTUAL_ENV', '')
    
    if not venv_path:
        return "Виртуальное окружение не активно. Пожалуйста, активируйте виртуальное окружение перед запуском."
    
    try:
        # Проверка наличия файла
        if not os.path.isfile(script_path):
            return "Файл скрипта не найден."
        
        # Запуск скрипта в виртуальном окружении
        script_name = os.path.basename(script_path)
        result = subprocess.run([f"{venv_path}/bin/python", script_name], cwd=os.path.dirname(script_path), capture_output=True, text=True)
        
        if result.returncode == 0:
            return f"Скрипт '{script_name}' успешно запущен:\n{result.stdout}"
        else:
            return f"Ошибка при запуске скрипта '{script_name}':\n{result.stderr}"
    except Exception as e:
        return f"Произошла ошибка при выполнении: {str(e)}"