# -*- coding: utf-8 -*-
NAME = "git_log"
DESCRIPTION = "Показывает последние коммиты git (история сохранений)."
PARAMS = {"path": "папка репозитория", "count": "сколько коммитов (по умолчанию 10)"}

import subprocess

def run(path=".", count="10"):
    path = path or "."
    try:
        n = str(int(str(count) or 10))
    except ValueError:
        n = "10"
    try:
        r = subprocess.run(
            ["git", "-C", path, "log", f"-{n}", "--pretty=format:%h  %ad  %s", "--date=short"],
            capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=30)
        if r.returncode != 0:
            return "Это не git-репозиторий или git не установлен:\n" + (r.stderr or "").strip()
        return r.stdout.strip() or "Коммитов пока нет."
    except FileNotFoundError:
        return "git не установлен в системе."
    except Exception as e:
        return f"Ошибка: {e}"
