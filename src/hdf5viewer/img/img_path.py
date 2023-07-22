import logging
import pathlib
import sys


def img_path() -> pathlib.Path:
    """
    Get path to img directory
    """
    if getattr(sys, "frozen", False):
        path = pathlib.Path(sys.executable).parent
        path = pathlib.Path(path, "img")
    else:
        path = pathlib.Path(__file__).absolute().parent

    logging.info(f"Image path '{path}'")

    return path
