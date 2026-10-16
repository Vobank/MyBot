# -*- coding: utf-8 -*-
NAME = "list_processes"
DESCRIPTION = "Показывает запущенные процессы, самые прожорливые по памяти сверху."
PARAMS = {"count": "сколько показать (по умолчанию 15)"}

import subprocess
import csv
import io

def run(count="15"):
    try:
        n = int(str(count) or 15)
    except ValueError:
        n = 15
    try:
        r = subprocess.run(["tasklist", "/fo", "csv", "/nh"],
                           capture_output=True, text=True, encoding="cp866",
                           errors="replace", timeout=30)
        rows = []
        for row in csv.reader(io.StringIO(r.stdout)):
            if len(row) >= 5:
                name = row[0]
                mem = row[4].replace("\xa0", "").replace(" ", "").replace("КБ", "").replace("K", "")
                mem = mem.replace(".", "").replace(",", "")
                try:
                    kb = int(mem)
                except ValueError:
                    kb = 0
                rows.append((kb, name))
        rows.sort(reverse=True)
        out = [f"{name}  —  {kb/1024:.0f} МБ" for kb, name in rows[:n]]
        return "\n".join(out) if out else "Не удалось получить список процессов."
    except FileNotFoundError:
        return "tasklist недоступен."
    except Exception as e:
        return f"Ошибка: {e}"
