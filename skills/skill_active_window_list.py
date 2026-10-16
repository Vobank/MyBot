import subprocess

NAME = "active_window_list"
DESCRIPTION = "возвращает список названий текущих активных окон"

def run(text=""):
    try:
        # Используем xprop для получения информации об окнах в Linux
        # В Windows можно использовать другие утилиты, такие как Get-Process в PowerShell
        result = subprocess.run(['xprop', '-root', '_NET_CLIENT_LIST'], stdout=subprocess.PIPE)
        window_ids = result.stdout.decode('utf-8').strip().split(',')[-1].strip()

        window_names = []
        for window_id in window_ids:
            result = subprocess.run(['xprop', '-id', window_id, 'WM_NAME'], stdout=subprocess.PIPE)
            name = result.stdout.decode('utf-8').split('=')[-1].strip().strip('"')
            window_names.append(name)

        return "\n".join(window_names)
    except Exception as e:
        return f"Не удалось получить список окон: {str(e)}"