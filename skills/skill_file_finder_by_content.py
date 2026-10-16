NAME = "file_finder_by_content"
DESCRIPTION = "Ищет файлы, содержащие указанный текст, в указанной папке."
PARAMS = {"text": "текст для поиска", "path": "папка для поиска (по умолчанию текущая)"}
DANGEROUS = False

def run(text="", path="."):
    import os

    if not text:
        return "Укажи, что искать."

    hits = []
    for root, _, files in os.walk(path or "."):
        for fn in files:
            fp = os.path.join(root, fn)
            try:
                with open(fp, encoding="utf-8", errors="ignore") as f:
                    if text in f.read():
                        hits.append(fp)
            except Exception as e:
                continue
            if len(hits) >= 100:
                return "\n".join(hits) + "\n... (обрезано)"
    return "\n".join(hits) if hits else "Ничего не найдено."