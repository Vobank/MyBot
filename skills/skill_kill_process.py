# -*- coding: utf-8 -*-
NAME = "kill_process"
DESCRIPTION = "Завершает процесс по имени (например notepad.exe). ОПАСНЫЙ."
PARAMS = {"name": "имя процесса, напр. notepad.exe"}
DANGEROUS = True

import subprocess

def run(name=""):
    name = (name or "").strip()
    if not name:
        return "Укажи имя процесса (например notepad.exe)."
    if not name.lower().endswith(".exe"):
        name += ".exe"
    try:
        r = subprocess.run(["taskkill", "/IM", name, "/F"],
                           capture_output=True, text=True, encoding="cp866",
                           errors="replace", timeout=30)
        return (r.stdout or r.stderr or "Готово.").strip()
    except Exception as e:
        return f"Ошибка: {e}"
