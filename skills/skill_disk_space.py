import shutil

NAME = "disk_space"
DESCRIPTION = "Показывает информацию о свободном и занятом пространстве на дисках"

def run(text=""):
    disk_usage = shutil.disk_usage("/")
    total = disk_usage.total // (2**30)  # в гигабайтах
    used = disk_usage.used // (2**30)
    free = disk_usage.free // (2**30)
    return f"Диск: Использовано {used} ГБ, Свободно {free} ГБ из {total} ГБ"