import sys
import pathlib


def img_path() -> pathlib.Path:
    """
    Get path to img directory
    """
    if getattr(sys, 'frozen', False):
        return pathlib.Path(sys.executable, "img")
    return pathlib.Path(__file__).absolute().parent
