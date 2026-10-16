NAME = "system_resource_report"
DESCRIPTION = "Создает краткий отчет о системных ресурсах (CPU, память, диски)."
PARAMS = {}
DANGEROUS = False

def run():
    import os
    import psutil

    report = "Отчет о системных ресурсах:\n\n"

    # CPU Usage
    cpu_percent = psutil.cpu_percent(interval=1)
    report += f"CPU Usage: {cpu_percent}%\n"

    # Memory Usage
    memory_info = psutil.virtual_memory()
    memory_percent = memory_info.percent
    memory_used = memory_info.used // (1024 * 1024)
    memory_total = memory_info.total // (1024 * 1024)
    report += f"Memory Usage: {memory_used} MB / {memory_total} MB ({memory_percent}%)\n"

    # Disk Usage
    partitions = psutil.disk_partitions()
    for partition in partitions:
        usage = psutil.disk_usage(partition.mountpoint)
        usage_percent = usage.percent
        usage_used = usage.used // (1024 * 1024 * 1024)
        usage_total = usage.total // (1024 * 1024 * 1024)
        report += f"Disk Usage ({partition.device}): {usage_used} GB / {usage_total} GB ({usage_percent}%)\n"

    return report