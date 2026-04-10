import json
import shutil
from pathlib import Path

from rules import sort_by_type, sort_by_date, sort_by_size
from undo_manager import save_action, undo_last, undo_all

with open("config.json") as f:
    config = json.load(f)


SORT_BY = config["sort_by"]


def get_single_folder():
    path = input("Enter folder path:\n").strip()
    folder = Path(path)

    if not folder.exists() or not folder.is_dir():
        print("❌ Invalid folder path")
        return None
    return folder


def get_multiple_folders():
    paths = input("Enter folder paths (comma separated):\n").split(",")

    folders = []
    for p in paths:
        folder = Path(p.strip())
        if folder.exists() and folder.is_dir():
            folders.append(folder)
        else:
            print(f"❌ Skipped invalid path: {p.strip()}")

    return folders


def get_target_directory():
    user_input = input("Enter folder path to organize : ").strip()

    if user_input:
        path = Path(user_input)
        if not path.exists() or not path.is_dir():
            print("❌ Invalid folder path")
            return None
        return path
    else:
        return Path(config["target_directory"])


def organize(target):
    for file in target.iterdir():
        if file.is_file():

            if SORT_BY == "type":
                folder = sort_by_type(file)

            elif SORT_BY == "date":
                folder = sort_by_date(file, config["date_format"])

            elif SORT_BY == "size":
                folder = sort_by_size(file, config["size_categories"])

            else:
                continue

            destination = target / folder
            destination.mkdir(exist_ok=True)

            new_path = destination / file.name
            save_action(str(file), str(new_path))
            shutil.move(str(file), str(new_path))


if __name__ == "__main__":

    while True:
        print("\n=== Smart File Organizer ===")
        print("1. Organize ONE folder")
        print("2. Organize MULTIPLE folders")
        print("3. Undo last file")
        print("4. Undo ALL changes")
        print("5. Exit")

        choice = input("Choose: ").strip()

        if choice == "1":
            folder = get_single_folder()
            if folder:
                organize(folder)
                print("Files organized successfully 🎯")

        elif choice == "2":
            folders = get_multiple_folders()
            if folders:
                for folder in folders:
                    organize(folder)
                print("Files organized successfully 🎯")

        elif choice == "3":
            undo_last()

        elif choice == "4":
            undo_all()

        elif choice == "5":
            print("Goodbye 👋")
            break

        else:
            print("❌ Invalid choice, try again")
