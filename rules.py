from pathlib import Path
from datetime import datetime

def sort_by_type(file_path):
    return file_path.suffix[1:].upper() or "NO_EXTENSION"


def sort_by_date(file_path, date_format):
    timestamp = file_path.stat().st_mtime
    return datetime.fromtimestamp(timestamp).strftime(date_format)


def sort_by_size(file_path, size_categories):
    size = file_path.stat().st_size

    for category, limit in size_categories.items():
        if size <= limit:
            return category

    return "Huge"

#