# -*- coding: utf-8 -*-
NAME = "git_status"
DESCRIPTION = "Показывает статус git-репозитория (изменённые/новые файлы)."
PARAMS = {"path": "папка репозитория (по умолчанию текущая)"}

import subprocess

def run(path="."):
    path = path or "."
    try:
        r = subprocess.run(["git", "-C", path, "status", "--short", "--branch"],
                           capture_output=True, text=True, encoding="utf-8",
                           errors="replace", timeout=30)
        if r.returncode != 0:
            return "Это не git-репозиторий или git не установлен:\n" + (r.stderr or "").strip()
        return r.stdout.strip() or "Чисто — изменений нет."
    except FileNotFoundError:
        return "git не установлен в системе."
    except Exception as e:
        return f"Ошибка: {e}"
