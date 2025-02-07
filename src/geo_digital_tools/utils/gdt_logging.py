"""Common logging system between Cygnets.

1. As library users (writers of scripts), we want log files that indicate our script status
2. As library developers, we want to be able to diagnose user applications

3. gdt and other libraries should not configure the logger.
4. Scripts should configure the logger.
5. A default logger configuration should be available to users IF they want to use it.
    - i.e. Document how to configure the gdt default logger in a script, but don't do it in the library.

https://docs.python.org/3/howto/logging.html#configuring-logging-for-a-library
"""

import copy
import logging
import logging.config
import logging.handlers
import sys
from pathlib import Path

from geo_digital_tools.utils.exceptions import KnownException

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def handle_exception(exc_type, exc_value, exc_traceback):
    """Ensure raised exceptions are logged."""
    if issubclass(exc_type, KeyboardInterrupt):
        # Allow KeyboardInterrupt to execute the standard excepthook
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    else:
        logger.critical(
            "Quit due to uncaught exception: ",
            exc_info=(exc_type, exc_value, exc_traceback),
        )


class KnownExceptionsFilter(logging.Filter):
    """Filter to capture log records that guide development of Cygnet Process/Steps.

    It triggers if a gdt.KnownException is included in the exc_info,
    or if "ERROR" is the level of the LogRecord.
    The modifications to the log only apply in KnownExceptions.log,
    (the handler the filter is attached to).

    """

    def filter(self, lr: logging.LogRecord):
        if (
            lr.levelname == "ERROR"  # TODO: Use custom logging level?
            or (lr.exc_info and type(lr.exc_info[1]).__name__ == "KnownException")
        ):
            # Capture exception and traceback
            lr_ = copy.copy(lr)
            lr_.msg = f"Raised: {repr(lr_.exc_info[1])}, with message '{lr_.message}'"
            lr_.exc_info = None  # (lr.exc_info[0], lr.exc_info[1], None)
            lr_.exc_text = None  #

            # Track count of this type of error?

            return lr_
        else:
            return False


def use_gdt_logging(log_dir: str | Path = "logs", use_excepthook: bool = False):
    """Configure logging to gdt recommendation.

    Args:
        log_dir: Directory to save logs in.
        use_excepthook: Use a custom exception hook (gdt_logging.handle_exception()).

    The preferred configuration is stdout and rotating logfiles.

    One logfile (KnownExceptions.log) captures data issues from Cygnet processes.
    This log can be used to interpret where the majority of files being processed
    fail, as a way to guide development.
    e.g., To notice that there are a large number of CSV files with an unusual delimiter.
    """
    log_dir = Path(log_dir)
    log_dir.mkdir(exist_ok=True, parents=True)

    standard_formatter = logging.Formatter(
        "%(name)s: %(asctime)s | %(levelname)s | %(filename)s:%(lineno)s  >>> %(message)s"
    )

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.WARNING)
    stdout_handler.setFormatter(standard_formatter)

    logfile_handler = logging.handlers.RotatingFileHandler(
        filename=log_dir / "gdt.log",
        mode="a",
        maxBytes=1_048_576,
        backupCount=2,
    )
    logfile_handler.setLevel(logging.INFO)
    logfile_handler.setFormatter(standard_formatter)

    ke_handler = logging.handlers.RotatingFileHandler(
        filename=log_dir / "KnownExceptions.log",
        mode="a",
        maxBytes=1_048_576,
        backupCount=2,
    )
    ke_handler.setFormatter(standard_formatter)
    ke_handler.addFilter(KnownExceptionsFilter())

    logger.setLevel(logging.INFO)

    logger.addHandler(stdout_handler)
    logger.addHandler(logfile_handler)
    logger.addHandler(ke_handler)

    logger.warning(
        f"Initialiased logger with gdt configuration. Writing to {log_dir.absolute()}."
    )

    if use_excepthook:
        # Insert exception handler
        sys.excepthook = handle_exception
        logger.warning("sys.excepthook has been modified to log raised errors.")
