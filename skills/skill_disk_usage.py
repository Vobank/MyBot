# -*- coding: utf-8 -*-
NAME = "disk_usage"
DESCRIPTION = "Показывает свободное и занятое место на дисках."
PARAMS = {}

import os
import shutil
import string

def run(**kwargs):
    lines = []
    for letter in string.ascii_uppercase:
        drive = f"{letter}:\\"
        if os.path.exists(drive):
            try:
                t, u, f = shutil.disk_usage(drive)
                gb = 1024 ** 3
                lines.append(f"{drive}  занято {u/gb:.1f} ГБ / всего {t/gb:.1f} ГБ  (свободно {f/gb:.1f} ГБ)")
            except Exception:
                pass
    return "\n".join(lines) if lines else "Диски не найдены."
