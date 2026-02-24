import logging
import time
from contextlib import contextmanager

LOG_FORMAT = "%(asctime)s [%(name)s] %(levelname)s: %(message)s"
DATE_FORMAT = "%H:%M:%S"

logging.basicConfig(level=logging.INFO, format=LOG_FORMAT, datefmt=DATE_FORMAT)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)


@contextmanager
def log_step(logger: logging.Logger, step: str):
    """Context manager that logs start/finish and duration of a step."""
    logger.info(f"▶ {step}")
    start = time.perf_counter()
    yield
    elapsed = time.perf_counter() - start
    logger.info(f"✔ {step} ({elapsed:.2f}s)")
