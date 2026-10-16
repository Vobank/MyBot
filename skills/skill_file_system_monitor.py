import os
import time

NAME = "file_system_monitor"
DESCRIPTION = "Отслеживает изменения в файловой системе для обнаружения новых файлов и директорий."

last_snapshot = {}

def take_snapshot(directory):
    snapshot = {}
    for root, dirs, files in os.walk(directory):
        snapshot[root] = {"dirs": set(dirs), "files": set(files)}
    return snapshot

def compare_snapshots(old_snapshot, new_snapshot):
    changes = []
    for path in set(old_snapshot.keys()) | set(new_snapshot.keys()):
        if path not in old_snapshot:
            changes.append(f"NEW DIR: {path}")
        elif path not in new_snapshot:
            changes.append(f"DELETED DIR: {path}")
        else:
            old_dirs, old_files = old_snapshot[path]["dirs"], old_snapshot[path]["files"]
            new_dirs, new_files = new_snapshot[path]["dirs"], new_snapshot[path]["files"]
            for dir_ in new_dirs - old_dirs:
                changes.append(f"NEW DIR: {os.path.join(path, dir_)}")
            for file_ in new_files - old_files:
                changes.append(f"NEW FILE: {os.path.join(path, file_)}")
    return changes

def run(directory=".", interval=5):
    global last_snapshot
    new_snapshot = take_snapshot(directory)
    changes = compare_snapshots(last_snapshot, new_snapshot)
    last_snapshot = new_snapshot
    return "\n".join(changes) if changes else "No changes detected."