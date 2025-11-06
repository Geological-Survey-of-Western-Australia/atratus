"""Common logging system between Cygnets.

1. As library users (writers of scripts), we want log files that indicate our script status
2. As library developers, we want to be able to diagnose user applications
3. gdt and other libraries should not configure the logger.
4. Scripts should configure the logger.
5. A default logger configuration should be available to users IF they want to use it.

With the above in mind, the logging submodule exists to configure the recommended logger,
 but doesn't do it automatically.

See this link for justification:
 https://docs.python.org/3/howto/logging.html#configuring-logging-for-a-library

"""

import copy
import logging
import logging.handlers
import sys
from pathlib import Path

from gswa_atratus.utils.exceptions import KnownException


class KnownExceptionsFilter(logging.Filter):
    """Filter which captures log records that guide development of Cygnet Process/Steps.

    It triggers if a gdt.KnownException is included in the exc_info,
    or if "ERROR" is the level of the LogRecord.
    The modifications to the log only apply in KnownExceptions.log, which is the handler
    the filter is attached to.
    """

    def filter(self, log_record: logging.LogRecord):
        if "KnownException" in log_record.msg:
            # Capture exception and traceback
            lr_ = copy.copy(log_record)
            if log_record.exc_info is not None:
                lr_.msg = f"{lr_.msg} -> {repr(lr_.exc_info[1])}"
                lr_.exc_info = None  # (lr.exc_info[0], lr.exc_info[1], None)
                lr_.exc_text = None
            return lr_
        else:
            return False


class NotKnownExceptionsFilter(logging.Filter):
    """Filter to exclude KnownException logs from general log.

    Performs the inverse of the KnownExceptionsFilter.
    """

    def filter(self, log_record: logging.LogRecord):
        if "KnownException" not in log_record.msg:
            return log_record


def use_gdt_logging(
    name: str | None = None,
    log_dir: str | Path = "logs",
    use_excepthook: bool = False,
):
    """Configure logging to gdt recommendation.

    Args:
        name: Name to provide to getLogger(name). None will use the global Root logger.
        log_dir: Directory to save log files to.
        use_excepthook: Use the gdt_logging.handle_exception() exception hook.

    The preferred configuration is to print to stdout and write to rotating logfiles.

    One logfile (KnownExceptions.log) captures data issues from Cygnet processes.
    This log can be used to interpret where the majority of files being processed
    fail, as a way to guide development.
    e.g., KnownException might trigger on CSV files with an unusual delimiter, but will
    allow continued execution of the calling program whilst logging the Exception.
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
