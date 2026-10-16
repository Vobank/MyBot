NAME = "window_manager_by_name"
DESCRIPTION = "Управляет окнами по названию приложения: сворачивает, разворачивает и закрывает их."
PARAMS = {"app_name": "название приложения", "action": "действие (minimize, maximize, close)"}
DANGEROUS = True

def run(app_name="", action="minimize"):
    import subprocess
    import re
    if not app_name:
        return "Укажи название приложения."
    if action not in ["minimize", "maximize", "close"]:
        return "Действие должно быть 'minimize', 'maximize' или 'close'."

    action_map = {"minimize": 6, "maximize": 3, "close": 0}
    hwnd = None

    try:
        # Получаем список окон
        EnumWindows = ctypes.windll.user32.EnumWindows
        EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
        GetWindowText = ctypes.windll.user32.GetWindowTextW
        GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
        IsWindowVisible = ctypes.windll.user32.IsWindowVisible

        titles = []

        def foreach_window(hwnd, lParam):
            if IsWindowVisible(hwnd):
                length = GetWindowTextLength(hwnd)
                buff = ctypes.create_unicode_buffer(length + 1)
                GetWindowText(hwnd, buff, length + 1)
                titles.append((hwnd, buff.value))
            return True

        EnumWindows(EnumWindowsProc(foreach_window), 0)

        # Находим hwnd нужного окна
        for hwnd, title in titles:
            if re.search(app_name, title):
                break
        else:
            return f"Окно с названием {app_name} не найдено."

        # Выполняем действие
        ctypes.windll.user32.ShowWindow(hwnd, action_map[action])
        return f"Окно {app_name} успешно {action}."

    except Exception as e:
        return f"Ошибка при выполнении действия: {str(e)}"