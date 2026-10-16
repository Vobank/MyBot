# -*- coding: utf-8 -*-
NAME = "git_diff"
DESCRIPTION = "Показывает несохранённые изменения в git (diff рабочей копии)."
PARAMS = {"path": "папка репозитория (по умолчанию текущая)"}

import subprocess

def run(path="."):
    path = path or "."
    try:
        r = subprocess.run(["git", "-C", path, "diff"],
                           capture_output=True, text=True, encoding="utf-8",
                           errors="replace", timeout=30)
        if r.returncode != 0:
            return "Это не git-репозиторий или git не установлен:\n" + (r.stderr or "").strip()
        out = r.stdout.strip()
        if not out:
            return "Изменений нет (всё сохранено или файлы новые — смотри git_status)."
        return out[:6000] + ("\n... (обрезано)" if len(out) > 6000 else "")
    except FileNotFoundError:
        return "git не установлен в системе."
    except Exception as e:
        return f"Ошибка: {e}"
