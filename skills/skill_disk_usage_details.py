NAME = "disk_usage_details"
DESCRIPTION = "Показывает подробную информацию о свободном и занятом месте на каждом разделе диска."
PARAMS = {}
DANGEROUS = False

def run():
    import os
    import psutil

    result = []
    partitions = psutil.disk_partitions()
    for partition in partitions:
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            result.append(f"Диск: {partition.device}")
            result.append(f"  Точка монтирования: {partition.mountpoint}")
            result.append(f"  Файловая система: {partition.fstype}")
            result.append(f"  Объем: {usage.total / (1024 ** 3):.2f} GB")
            result.append(f"  Использовано: {usage.used / (1024 ** 3):.2f} GB")
            result.append(f"  Свободно: {usage.free / (1024 ** 3):.2f} GB")
            result.append(f"  Процент использования: {usage.percent}%")
            result.append("-" * 30)
        except PermissionError:
            # игнорируем разделы, к которым нет доступа
            continue
    return "\n".join(result) if result else "Нет информации о дисках."