# -*- coding: utf-8 -*-
NAME = "backup_folder"
DESCRIPTION = "Делает zip-резервную копию папки (в подпапку backups рядом с ней)."
PARAMS = {"path": "папка, которую сохранить"}

import os
import shutil
import time

def run(path=""):
    path = (path or "").strip()
    if not path:
        return "Укажи папку для резервной копии."
    if not os.path.isdir(path):
        return f"Папка не найдена: {path}"
    parent = os.path.dirname(os.path.abspath(path)) or "."
    backups = os.path.join(parent, "backups")
    os.makedirs(backups, exist_ok=True)
    base = os.path.join(backups, os.path.basename(os.path.abspath(path)) + "_" + time.strftime("%Y%m%d_%H%M%S"))
    try:
        archive = shutil.make_archive(base, "zip", path)
        size = os.path.getsize(archive) / (1024 * 1024)
        return f"Готово: {archive} ({size:.1f} МБ)"
    except Exception as e:
        return f"Ошибка: {e}"
