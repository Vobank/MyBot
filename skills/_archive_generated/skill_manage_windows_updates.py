NAME = "manage_windows_updates"
DESCRIPTION = "Управляет автоматическим обновлением установленных программ через Windows Update."
PARAMS = {"action": "действие (check, download, install)"}
DANGEROUS = True

def run(action="check"):
    import subprocess

    if action not in ["check", "download", "install"]:
        return "Действие должно быть 'check', 'download' или 'install'."

    try:
        if action == "check":
            result = subprocess.run(["powershell", "Get-WindowsUpdateLog"], capture_output=True, text=True)
            return result.stdout
        elif action == "download":
            result = subprocess.run(["powershell", "Invoke-WindowsUpdateDownload"], capture_output=True, text=True)
            return result.stdout
        elif action == "install":
            result = subprocess.run(["powershell", "Invoke-WindowsUpdateInstall"], capture_output=True, text=True)
            return result.stdout
    except Exception as e:
        return f"Произошла ошибка: {str(e)}"

    return "Неизвестное действие."