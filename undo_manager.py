import json
import shutil
from pathlib import Path

HISTORY_FILE = "history.json"

def cleanup_empty_folders(base_dir):
    """
    Recursively remove empty folders inside base_dir
    """
    base_dir = Path(base_dir)

    if not base_dir.exists():
        return

    for path in sorted(base_dir.rglob("*"), reverse=True):
        if path.is_dir() and not any(path.iterdir()):
            path.rmdir()



def load_history():
    if not Path(HISTORY_FILE).exists():
        return []

    try:
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []


def save_action(original, moved):
    data = load_history()
    data.append({"from": original, "to": moved})

    with open(HISTORY_FILE, "w") as f:
        json.dump(data, f, indent=4)


def undo_last():
    data = load_history()

    if not data:
        print("Nothing to undo ❌")
        return

    last = data.pop()

    from_path = Path(last["from"])
    to_path = Path(last["to"])

    if to_path.exists():
        shutil.move(str(to_path), str(from_path))

    with open(HISTORY_FILE, "w") as f:
        json.dump(data, f, indent=4)

    cleanup_empty_folders(from_path.parent)
    print("Last action undone ✅")



def undo_all():
    data = load_history()

    if not data:
        print("Nothing to undo ❌")
        return

    affected_dirs = set()

    for action in reversed(data):
        from_path = Path(action["from"])
        to_path = Path(action["to"])

        if to_path.exists():
            shutil.move(str(to_path), str(from_path))
            affected_dirs.add(from_path.parent)

    with open(HISTORY_FILE, "w") as f:
        json.dump([], f, indent=4)

    for d in affected_dirs:
        cleanup_empty_folders(d)

    print("All changes undone 🔁")


