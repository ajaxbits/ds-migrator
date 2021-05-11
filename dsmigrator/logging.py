import logging
from datetime import datetime

from rich.console import Console
from rich.logging import RichHandler

console = Console(log_path=False)
error_console = True

LOG_FILE_FORMAT = logging.Formatter("%(asctime)s — %(levelname)s — %(message)s")
LOG_FILE = datetime.now().strftime("dsmigrator_%H_%M_%d_%m_%Y.log")


def get_file_handler():
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setFormatter(LOG_FILE_FORMAT)
    return file_handler


def get_console_handler():
    stream_handler = RichHandler(console=console, show_path=False)
    stream_handler.setLevel(logging.INFO)
    return stream_handler


logging.basicConfig(
    level="DEBUG",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[
        get_console_handler(),
        get_file_handler(),
    ],
)

log = logging.getLogger("dsmigrator")
