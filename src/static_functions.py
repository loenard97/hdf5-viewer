import os


def file_size_to_str(file_path: str) -> str:
    """
    Get formated File Size
    """
    size = os.path.getsize(file_path)

    if size > 1024**3:
        return f"{size/1024**3:.2f} GB"
    elif size > 1024**2:
        return f"{size/1024**2:.2f} MB"
    elif size > 1024:
        return f"{size/1024:.2f} kB"
    else:
        return f"{size} bytes"
