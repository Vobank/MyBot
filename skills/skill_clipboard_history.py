NAME = "clipboard_history"
DESCRIPTION = "Сохраняет и показывает историю текста из буфера обмена."
PARAMS = {"limit": "ограничение на количество сохраненных элементов (по умолчанию 10)"}
DANGEROUS = False

def run(limit=10):
    import os
    import json
    from datetime import datetime

    history_file = "clipboard_history.json"
    
    if not os.path.exists(history_file):
        with open(history_file, "w") as f:
            json.dump([], f)
    
    with open(history_file, "r") as f:
        history = json.load(f)

    if len(history) > limit:
        history = history[-limit:]

    result = "\n".join([f"{entry['timestamp']} - {entry['text']}" for entry in history])
    
    return result if result else "История буфера обмена пуста."