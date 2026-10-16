NAME = "network_resource_report"
DESCRIPTION = "Создает отчет о доступных сетевых ресурсах (серверах и файлах)."
PARAMS = {"path": "путь к сетевому ресурсу (по умолчанию \\\\localhost}"}
DANGEROUS = False

def run(path="\\\\localhost"):
    try:
        import os
        report = []
        if not path:
            return "Укажи путь к сетевому ресурсу."
        
        for root, dirs, files in os.walk(path):
            report.append(f"Директория: {root}")
            for d in dirs:
                report.append(f"  Папка: {d}")
            for f in files:
                report.append(f"  Файл: {f}")
            if len(report) > 100:
                report.append("... (обрезано)")
                break
        return "\n".join(report)
    except Exception as e:
        return f"Ошибка: {str(e)}"