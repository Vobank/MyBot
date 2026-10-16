import os

NAME = "show_disk_usage"
DESCRIPTION = "Показывает свободное и занятое пространство на диске по конкретному пути."

def run(path="."):
    total, used, free = shutil.disk_usage(path)
    result = (f"Для пути {path}:\n"
              f"Всего: {total // (2**30)} ГБ\n"
              f"Занято: {used // (2**30)} ГБ\n"
              f"Свободно: {free // (2**30)} ГБ")
    return result