import difflib

NAME = "show_diff_files"
DESCRIPTION = "Показывает различия между двумя версиями файлов в формате diff."

def run(text=""):
    if not text:
        return "Необходимо указать два пути к файлам."
    
    file_paths = text.split()
    if len(file_paths) != 2:
        return "Необходимо указать два пути к файлам."
    
    file1_path, file2_path = file_paths
    
    try:
        with open(file1_path, 'r', encoding='utf-8') as file1:
            with open(file2_path, 'r', encoding='utf-8') as file2:
                file1_content = file1.readlines()
                file2_content = file2.readlines()
                
                diff = difflib.unified_diff(file1_content, file2_content, fromfile=file1_path, tofile=file2_path)
                diff_result = '\n'.join(diff)
                return diff_result
    except Exception as e:
        return f"Ошибка при чтении файлов: {str(e)}"