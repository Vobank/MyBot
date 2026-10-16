import os

NAME = "code_project_analysis"
DESCRIPTION = "Анализирует проект и вычисляет количество строк кода, комментариев и пустых строк."

def run(text=""):
    directory = text.strip() if text.strip() else '.'
    lines_of_code = 0
    lines_of_comments = 0
    empty_lines = 0

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                    for line in f:
                        stripped_line = line.strip()
                        if stripped_line:
                            if stripped_line.startswith('#'):
                                lines_of_comments += 1
                            else:
                                lines_of_code += 1
                        else:
                            empty_lines += 1

    result = (f"Количество строк кода: {lines_of_code}\n"
              f"Количество строк комментариев: {lines_of_comments}\n"
              f"Количество пустых строк: {empty_lines}")
    return result