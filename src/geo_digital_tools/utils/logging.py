import logging
from pathlib import Path

# import opentelemetry-distro


def setup_logger(
    name: str,
    log_file: Path,
    level: int = 10,
    logging_format: str = "%(asctime)s %(levelname)s %(message)s",
    deployed: bool = False,
) -> logging.Logger:
    """
    Generates a logger and specifies the formatting.
    """
    formatter = logging.Formatter(logging_format)
    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    # if deployed:
    #     logger.addHandler(AzureLogHandler()
    #                       )

    return logger


def find_valid_logger(logger_id: str, default_logging_dir : Path = Path("logs")) -> logging.Logger:
    """
    In a running session searches for a specified logger.
    If none found generates a new failover logger.
    """
    Path(default_logging_dir).mkdir(parents=True, exist_ok=True)
    fail_name = f"Fail_Over - {logger_id}"
    desired_loggers = [logger_id, fail_name]
    active_loggers = list(logging.Logger.manager.loggerDict.keys())
    check_result = [x for x in desired_loggers if x in active_loggers]

    if len(check_result) == 0:
        # if none of the loggers exist
        logger = setup_logger(fail_name, default_logging_dir / f"{fail_name}.log")
    else:
        # if they do exist get the first one
        logger = logging.getLogger(check_result[0])

    return logger
