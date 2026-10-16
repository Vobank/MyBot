NAME = "show_file_content_range"
DESCRIPTION = "Показывает содержимое текстового файла построчно с возможностью указать диапазон строк."
PARAMS = {"file_path": "путь к файлу", "start_line": "начальная строка (по умолчанию 1)", "end_line": "конечная строка (по умолчанию последняя строка)"}
def run(file_path="", start_line=1, end_line=-1):
    try:
        if not file_path:
            return "Укажи путь к файлу."
        
        with open(file_path, encoding="utf-8", errors="ignore") as file:
            lines = file.readlines()
        
        if start_line < 1:
            start_line = 1
        
        if end_line == -1 or end_line > len(lines):
            end_line = len(lines)
        
        if start_line > end_line:
            return "Начальная строка больше конечной строки."
        
        content = ''.join(lines[start_line-1:end_line])
        return content
    except FileNotFoundError:
        return "Файл не найден."
    except Exception as e:
        return f"Произошла ошибка: {str(e)}"