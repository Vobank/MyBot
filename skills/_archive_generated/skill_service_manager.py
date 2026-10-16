NAME = "service_manager"
DESCRIPTION = "Управляет службами Windows: запускает, останавливает и показывает их статус."
PARAMS = {"action": "действие (start, stop, status)", "service_name": "имя службы"}

DANGEROUS = True

def run(action="status", service_name=""):
    import subprocess

    if not service_name:
        return "Укажи имя службы."

    actions = {
        "start": "start",
        "stop": "stop",
        "status": "query"
    }

    if action not in actions:
        return "Недопустимое действие. Используй start, stop или status."

    try:
        cmd = f'sc query {service_name}'
        if action != "status":
            cmd = f'sc {actions[action]} {service_name}'
        result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
        if result.returncode != 0:
            return f"Ошибка при выполнении действия {action} для службы {service_name}: {result.stderr}"
        return result.stdout
    except Exception as e:
        return f"Произошла ошибка: {str(e)}"