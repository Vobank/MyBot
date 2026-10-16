NAME = "monitor_cpu_memory_usage"
DESCRIPTION = "Собирает и анализирует информацию о загрузке процессора и оперативной памяти."
PARAMS = {}

def run():
    import os
    import psutil
    import datetime
    
    try:
        # Получаем информацию о загрузке процессора
        cpu_usage = psutil.cpu_percent(interval=1)
        
        # Получаем информацию о загрузке оперативной памяти
        memory_info = psutil.virtual_memory()
        memory_usage = memory_info.percent
        memory_used = memory_info.used / (1024**3)  # в гигабайтах
        memory_total = memory_info.total / (1024**3)  # в гигабайтах
        
        # Формируем результат
        result = f"Время сбора данных: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        result += f"Загрузка процессора: {cpu_usage}%\n"
        result += f"Использование оперативной памяти: {memory_usage}%\n"
        result += f"Использовано памяти: {memory_used:.2f} ГБ из {memory_total:.2f} ГБ\n"
        
        return result
    except Exception as e:
        return f"Произошла ошибка: {str(e)}"