import logging
from rich.console import Console, OverflowMethod
from rich.logging import RichHandler
from rich.traceback import install

FORMAT = "%(message)s"
logging.basicConfig(
    level="WARNING",
    format=FORMAT,
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)],
)
log = logging.getLogger("rich")

console = Console(record=True)