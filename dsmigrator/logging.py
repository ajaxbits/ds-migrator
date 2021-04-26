import logging
from datetime import datetime
from rich.console import Console
from rich.logging import RichHandler

filename = datetime.now().strftime("dsmigrator_%H_%M_%d_%m_%Y.log")

console = Console(record=True, log_path=False)
error_console = Console(record=True, stderr=True)
FORMAT = "%(message)s"
logging.basicConfig(
    level="WARNING",
    format=FORMAT,
    datefmt="[%X]",
    handlers=[
        RichHandler(
            rich_tracebacks=True, tracebacks_show_locals=True, console=error_console
        )
    ],
)
log = logging.getLogger("rich")
