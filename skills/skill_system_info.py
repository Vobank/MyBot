# -*- coding: utf-8 -*-
NAME = "system_info"
DESCRIPTION = "Показывает сведения о системе: ОС, процессор, оперативная память."
PARAMS = {}

import os
import platform
import ctypes

def run(**kwargs):
    info = []
    info.append(f"ОС: {platform.system()} {platform.release()} ({platform.version()})")
    info.append(f"Процессор: {platform.processor() or 'н/д'}")
    info.append(f"Ядер (логических): {os.cpu_count()}")
    try:
        class M(ctypes.Structure):
            _fields_ = [("dwLength", ctypes.c_ulong), ("dwMemoryLoad", ctypes.c_ulong),
                        ("ullTotalPhys", ctypes.c_ulonglong), ("ullAvailPhys", ctypes.c_ulonglong),
                        ("ullTotalPageFile", ctypes.c_ulonglong), ("ullAvailPageFile", ctypes.c_ulonglong),
                        ("ullTotalVirtual", ctypes.c_ulonglong), ("ullAvailVirtual", ctypes.c_ulonglong),
                        ("ullAvailExtendedVirtual", ctypes.c_ulonglong)]
        m = M()
        m.dwLength = ctypes.sizeof(M)
        ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m))
        gb = 1024 ** 3
        info.append(f"Память: занято {m.dwMemoryLoad}% | "
                    f"всего {m.ullTotalPhys/gb:.1f} ГБ, свободно {m.ullAvailPhys/gb:.1f} ГБ")
    except Exception:
        pass
    return "\n".join(info)
