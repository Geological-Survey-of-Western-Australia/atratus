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


class KnownExceptionsFilter(logging.Filter):
    """Filter to capture log records that guide development of Cygnet Process/Steps.

    It triggers if a gdt.KnownException is included in the exc_info,
    or if "ERROR" is the level of the LogRecord.
    The modifications to the log only apply in KnownExceptions.log,
    (the handler the filter is attached to).
    """

    def filter(self, lr: logging.LogRecord):
        if "KnownException" in lr.msg:
            # Capture exception and traceback
            lr_ = copy.copy(lr)
            if lr.exc_info is not None:
                lr_.msg = f"{lr_.msg} -> {repr(lr_.exc_info[1])}"
                lr_.exc_info = None  # (lr.exc_info[0], lr.exc_info[1], None)
                lr_.exc_text = None
            return lr_
        else:
            return False


class NotKnownExceptionsFilter(logging.Filter):
    """Filter to exclude KnownException logs from general log."""

    def filter(self, lr: logging.LogRecord):
        if "KnownException" not in lr.msg:
            return lr


def use_gdt_logging(
    name: str | None = None,
    log_dir: str | Path = "logs",
    use_excepthook: bool = False,
):
    """Configure logging to gdt recommendation.

    Args:
        name: Name to provide to getLogger(name). None for Root logger.
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

    # Standard output logs of WARNING or above.
    standard_formatter = logging.Formatter(
        "%(asctime)s: %(name)s:%(lineno)s | %(levelname)s | %(message)s"
    )

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.WARNING)
    stdout_handler.setFormatter(standard_formatter)
    stdout_handler.addFilter(NotKnownExceptionsFilter())

    # Logfile that captures all program logs EXCEPT KnownException
    logfile_handler = logging.handlers.RotatingFileHandler(
        filename=log_dir / "gdt.log",
        mode="w",
        maxBytes=1_048_576,
        backupCount=2,
    )
    logfile_handler.setLevel(logging.INFO)
    logfile_handler.setFormatter(standard_formatter)
    logfile_handler.addFilter(NotKnownExceptionsFilter())

    #  Logfile that captures only KnownException logs
    ke_handler = logging.handlers.RotatingFileHandler(
        filename=log_dir / "KnownExceptions.log",
        mode="w",
        maxBytes=1_048_576,
        backupCount=2,
    )
    ke_handler.setLevel(logging.INFO)
    ke_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s: %(process_)s.%(step_)s.%(funcName)s | '%(input_)s' | %(message)s"
        )
    )
    ke_handler.addFilter(KnownExceptionsFilter())

    # Initialise root logger.
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(stdout_handler)
    logger.addHandler(logfile_handler)
    logger.addHandler(ke_handler)

    logger.warning(
        f"Initialiased root logger with gdt configuration. Writing to {log_dir.absolute()}."
    )

    if use_excepthook:

        def _handle_exception(exc_type, exc_value, exc_traceback):
            """Log the unhandled exception that caused code to exit."""
            if issubclass(exc_type, KeyboardInterrupt):
                # Allow KeyboardInterrupt to execute the standard excepthook
                sys.__excepthook__(exc_type, exc_value, exc_traceback)
                return
            else:
                logger.critical(
                    "Quit due to uncaught exception: ",
                    exc_info=(exc_type, exc_value, exc_traceback),
                )

        sys.excepthook = _handle_exception
        logger.warning("sys.excepthook has been modified to log raised errors.")

    return logger
