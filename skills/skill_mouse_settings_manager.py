NAME = "mouse_settings_manager"
DESCRIPTION = "Управляет настройками мыши: скорость указателя, включение или выключение прокрутки колеса."
PARAMS = {
    "speed": "новая скорость указателя (1-20)",
    "scroll": "включить (1) или выключить (0) прокрутку колеса"
}
DANGEROUS = True

def run(speed=None, scroll=None):
    import subprocess
    result = ""
    
    if speed is not None:
        try:
            speed = int(speed)
            if 1 <= speed <= 20:
                subprocess.run(['mouse_speed', str(speed)], check=True)
                result += f"Скорость указателя мыши установлена на {speed}.\n"
            else:
                result += "Скорость указателя должна быть в диапазоне от 1 до 20.\n"
        except Exception as e:
            result += f"Ошибка при изменении скорости указателя: {str(e)}\n"
    
    if scroll is not None:
        try:
            scroll = int(scroll)
            if scroll == 0 or scroll == 1:
                subprocess.run(['mouse_scroll', str(scroll)], check=True)
                result += f"Прокрутка колеса мыши {'включена' if scroll else 'выключена'}.\n"
            else:
                result += "Прокрутка колеса мыши должна быть включена (1) или выключена (0).\n"
        except Exception as e:
            result += f"Ошибка при изменении прокрутки колеса: {str(e)}\n"
    
    if not result:
        return "Нет изменений."
    else:
        return result