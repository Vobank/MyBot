# -*- coding: utf-8 -*-
NAME = "grep_text"
DESCRIPTION = "Ищет строки по шаблону в файлах папки (как grep)."
PARAMS = {"pattern": "что искать (текст или регэксп)", "path": "папка (по умолчанию текущая)"}

import os
import re

def run(pattern="", path="."):
    if not pattern:
        return "Укажи, что искать."
    path = path or "."
    try:
        rx = re.compile(pattern, re.IGNORECASE)
    except re.error:
        rx = re.compile(re.escape(pattern), re.IGNORECASE)
    hits = []
    for root, _, files in os.walk(path):
        for fn in files:
            fp = os.path.join(root, fn)
            try:
                for i, line in enumerate(open(fp, encoding="utf-8", errors="ignore"), 1):
                    if rx.search(line):
                        hits.append(f"{fp}:{i}: {line.strip()[:200]}")
                        if len(hits) >= 100:
                            return "\n".join(hits) + "\n... (обрезано на 100)"
            except Exception:
                pass
    return "\n".join(hits) if hits else "Ничего не найдено."
