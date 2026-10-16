NAME = "bookmark_manager"
DESCRIPTION = "Управляет закладками в браузере: добавляет, удаляет и показывает список."
PARAMS = {"action": "действие (add, remove, list)", "url": "URL-адрес (для добавления и удаления)", "title": "название закладки (для добавления)"}
DANGEROUS = True

def run(action="list", url="", title=""):
    import json
    from collections import defaultdict

    bookmarks_file = os.path.expanduser("~/.bookmarks.json")
    bookmarks = defaultdict(list)

    if os.path.exists(bookmarks_file):
        with open(bookmarks_file, "r") as f:
            bookmarks = json.load(f)

    if action == "add":
        if not url or not title:
            return "Укажите URL и название для добавления закладки."
        bookmarks[title].append(url)
        with open(bookmarks_file, "w") as f:
            json.dump(bookmarks, f, indent=4)
        return f"Закладка '{title}' добавлена."

    elif action == "remove":
        if not url:
            return "Укажите URL для удаления закладки."
        removed = False
        for title, urls in bookmarks.items():
            if url in urls:
                urls.remove(url)
                removed = True
        if removed:
            with open(bookmarks_file, "w") as f:
                json.dump(bookmarks, f, indent=4)
            return "Закладка удалена."
        else:
            return "Закладка не найдена."

    elif action == "list":
        if not bookmarks:
            return "Список закладок пуст."
        return "\n".join([f"{title}: {urls}" for title, urls in bookmarks.items()])

    else:
        return "Неизвестное действие. Используйте add, remove или list."