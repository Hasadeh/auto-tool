import logging
import sys
from pathlib import Path


class MemoryLogHandler(logging.Handler):
    def __init__(self) -> None:
        super().__init__()
        self.records: list[str] = []

    def emit(self, record: logging.LogRecord) -> None:
        self.records.append(self.format(record))


def setup_logging(log_dir: Path) -> tuple[logging.Logger, MemoryLogHandler]:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "check.log"
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    logger = logging.getLogger("check_list")
    logger.setLevel(logging.DEBUG)
    memory_handler = _existing_memory_handler(logger)
    if memory_handler:
        return logger, memory_handler

    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    memory_handler = MemoryLogHandler()
    memory_handler.setLevel(logging.DEBUG)
    memory_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    logger.addHandler(memory_handler)
    return logger, memory_handler


def _existing_memory_handler(logger: logging.Logger) -> MemoryLogHandler | None:
    for handler in logger.handlers:
        if isinstance(handler, MemoryLogHandler):
            return handler
    return None
