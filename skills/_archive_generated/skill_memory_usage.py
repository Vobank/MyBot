NAME = "memory_usage"
DESCRIPTION = "Показывает информацию о загрузке оперативной памяти."
PARAMS = {}
DANGEROUS = False

def run():
    import os
    import psutil

    try:
        virtual_memory = psutil.virtual_memory()
        total_memory = virtual_memory.total / (1024 ** 3)
        used_memory = virtual_memory.used / (1024 ** 3)
        free_memory = virtual_memory.free / (1024 ** 3)
        memory_percent = virtual_memory.percent

        result = (
            f"Загрузка оперативной памяти:\n"
            f"Общая память: {total_memory:.2f} ГБ\n"
            f"Используется: {used_memory:.2f} ГБ\n"
            f"Свободно: {free_memory:.2f} ГБ\n"
            f"Загрузка: {memory_percent}%"
        )
    except Exception as e:
        result = f"Ошибка: {str(e)}"

    return result