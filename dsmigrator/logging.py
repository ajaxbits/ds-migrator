import logging
from datetime import datetime
from rich.console import Console
from rich.logging import RichHandler

filename = datetime.now().strftime("dsmigrator_%H_%M_%d_%m_%Y.log")

console = Console(record=True, log_path=False)
error_console = Console(record=True, stderr=True)

STDOUT_FORMAT = "%(message)s"
LOG_FILE_FORMAT = logging.Formatter(
    "%(asctime)s — %(name)s — %(levelname)s — %(message)s"
)


def get_file_handler():
    file_handler = logging.FileHandler("alex.log")
    file_handler.setFormatter(LOG_FILE_FORMAT)
    file_handler.setLevel(logging.DEBUG)
    return file_handler


logging.basicConfig(
    level="INFO",
    format=STDOUT_FORMAT,
    datefmt="[%X]",
    handlers=[
        RichHandler(rich_tracebacks=True, tracebacks_show_locals=True, console=console),
        get_file_handler(),
    ],
)
log = logging.getLogger("rich")
