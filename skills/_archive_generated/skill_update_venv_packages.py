NAME = "update_venv_packages"
DESCRIPTION = "Автоматически обновляет все установленные пакеты Python в указанном виртуальном окружении."
PARAMS = {"venv_path": "путь к виртуальному окружению"}
DANGEROUS = True

def run(venv_path="."):
    try:
        import os
        activate_script = os.path.join(venv_path, "Scripts", "activate") if os.name == "nt" else os.path.join(venv_path, "bin", "activate")
        command = f"source {activate_script} && python -m pip list --outdated --format=freeze | grep -v '^\-e' | cut -d = -f 1  | xargs -n1 python -m pip install --upgrade"
        if os.name == "nt":
            command = f"{activate_script} && python -m pip list --outdated --format=freeze | findstr /v \"-e\" | cut -d = -f 1  | xargs -n1 python -m pip install --upgrade"
        result = os.popen(command).read()
        return f"Успешно обновлены пакеты в виртуальном окружении {venv_path}.\n{result}"
    except Exception as e:
        return f"Произошла ошибка при обновлении пакетов: {str(e)}"