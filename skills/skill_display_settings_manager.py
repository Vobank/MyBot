NAME = "display_settings_manager"
DESCRIPTION = "Показывает и управляет настройками дисплея (разрешение, частота обновления)."
PARAMS = {
    "action": "действие: 'show' (показать текущие настройки), 'set' (установить новые настройки)",
    "resolution": "новое разрешение в формате 'ширинаxвысота', например '1920x1080'",
    "refresh_rate": "новая частота обновления в Гц, например '60'"
}
DANGEROUS = True

def run(action="show", resolution=None, refresh_rate=None):
    import subprocess
    result = ""
    
    if action == "show":
        try:
            output = subprocess.check_output(["powershell", "-Command", "(Get-WmiObject -Class Win32_VideoController).CurrentResolution + 'x' + (Get-WmiObject -Class Win32_VideoController).CurrentVerticalResolution + ' ' + (Get-WmiObject -Class Win32_VideoController).CurrentRefreshRate"], universal_newlines=True)
            result = f"Текущие настройки: {output.strip()}"
        except Exception as e:
            result = f"Ошибка при получении настроек: {e}"
    elif action == "set":
        if resolution and refresh_rate:
            try:
                subprocess.check_output(["powershell", "-Command", f"(Get-WmiObject -Class CIM_VideoControllerSetting).SetResolution({resolution.split('x')[0]}, {resolution.split('x')[1]}, {refresh_rate})"], universal_newlines=True)
                result = f"Настройки успешно установлены: {resolution} {refresh_rate} Гц"
            except Exception as e:
                result = f"Ошибка при установке настроек: {e}"
        else:
            result = "Для установки настроек необходимо указать разрешение и частоту обновления."
    else:
        result = "Укажите корректное действие ('show' или 'set')."
    
    return result