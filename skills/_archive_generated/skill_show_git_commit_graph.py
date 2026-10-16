import os
import subprocess
import graphviz

NAME = "show_git_commit_graph"
DESCRIPTION = "Отображает историю коммитов в виде графа."

def run(text=""):
    try:
        # Получаем историю коммитов
        result = subprocess.run(["git", "log", "--oneline", "--graph"], capture_output=True, text=True, check=True)
        log_output = result.stdout

        # Создаем граф
        graph = graphviz.Digraph(format='png')
        commits = log_output.split('\n')
        for commit in commits:
            if commit:
                graph.node(commit[:7], commit[8:])
                if len(commit) > 7 and commit[7] == '|':
                    parent = commits[commits.index(commit) - 1]
                    if parent and len(parent) > 7:
                        graph.edge(parent[:7], commit[:7])

        # Сохраняем и отображаем граф
        graph.render('git_commit_graph', view=True)
        return "Граф коммитов успешно создан и открыт."
    except subprocess.CalledProcessError as e:
        return f"Ошибка при выполнении git log: {e.stderr}"
    except Exception as e:
        return f"Произошла ошибка: {str(e)}"