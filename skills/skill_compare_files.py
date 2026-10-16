import difflib

NAME = "compare_files"
DESCRIPTION = "сравнивает содержимое двух файлов и показывает различия"

def run(file1_path, file2_path):
    try:
        with open(file1_path, 'r', encoding='utf-8') as file1:
            file1_lines = file1.readlines()
        with open(file2_path, 'r', encoding='utf-8') as file2:
            file2_lines = file2.readlines()

        diff = difflib.unified_diff(file1_lines, file2_lines, fromfile=file1_path, tofile=file2_path)
        diff_result = '\n'.join(list(diff))

        if diff_result:
            return f"Различия между файлами:\n{diff_result}"
        else:
            return "Файлы идентичны"
    except Exception as e:
        return f"Произошла ошибка при сравнении файлов: {str(e)}"