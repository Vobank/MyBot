import os
import difflib
import filecmp

NAME = "directory_diff"
DESCRIPTION = "Сравнивает содержимое двух директорий и показывает различия"

def run(dir1="", dir2=""):
    if not os.path.isdir(dir1) or not os.path.isdir(dir2):
        return "Одна из указанных директорий не существует."
    
    # Сравниваем содержимое директорий
    dir_cmp = filecmp.dircmp(dir1, dir2)
    
    result = []
    result.append(f"Файлы, присутствующие только в {dir1}: {dir_cmp.left_only}")
    result.append(f"Файлы, присутствующие только в {dir2}: {dir_cmp.right_only}")
    
    common_files = dir_cmp.common_files
    for file in common_files:
        file1 = os.path.join(dir1, file)
        file2 = os.path.join(dir2, file)
        
        with open(file1, 'r', encoding='utf-8', errors='ignore') as f1, \
             open(file2, 'r', encoding='utf-8', errors='ignore') as f2:
            diff = difflib.unified_diff(f1.readlines(), f2.readlines(), fromfile=file1, tofile=file2)
            diff_result = '\n'.join(diff)
            
        if diff_result:
            result.append(f"Различия в файле {file}:")
            result.append(diff_result)
    
    return '\n'.join(result)