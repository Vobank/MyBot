import difflib

NAME = "show_diff"
DESCRIPTION = "Показывает различия между двумя текстовыми файлами"

def run(file1_path="", file2_path=""):
    try:
        with open(file1_path, 'r') as file1, open(file2_path, 'r') as file2:
            file1_lines = file1.readlines()
            file2_lines = file2.readlines()

        diff = difflib.unified_diff(file1_lines, file2_lines, fromfile=file1_path, tofile=file2_path)
        diff_result = '\n'.join(diff)
        return diff_result
    except Exception as e:
        return f"Ошибка при чтении файлов или вычислении различий: {str(e)}"