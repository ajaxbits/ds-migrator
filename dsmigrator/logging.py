import logging
from datetime import datetime
from rich.console import Console
from rich.logging import RichHandler

filename = datetime.now().strftime("dsmigrator_%H_%M_%d_%m_%Y.log")

console = Console(record=True, log_path=False)
error_console = Console(record=True, stderr=True)

STDOUT_FORMAT = "%(message)s"
LOG_FILE_FORMAT = logging.Formatter("%(asctime)s — %(levelname)s — %(message)s")


def get_file_handler():
    file_handler = logging.FileHandler("alex.log")
    file_handler.setFormatter(LOG_FILE_FORMAT)
    return file_handler


def get_stream_handler():
    stream_handler = RichHandler(console=console)
    stream_handler.setLevel(logging.INFO)
    return stream_handler


logging.basicConfig(
    level="DEBUG",
    format=STDOUT_FORMAT,
    datefmt="[%X]",
    handlers=[
        get_stream_handler(),
        get_file_handler(),
    ],
)
log = logging.getLogger("dsmigrator")
