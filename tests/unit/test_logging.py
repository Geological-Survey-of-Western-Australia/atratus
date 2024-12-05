import logging
import pytest
from pathlib import Path
from geo_digital_tools.utils.logging import setup_logger, find_valid_logger


@pytest.fixture
def temp_log_dir():
    """
    Fixture for creating and cleaning up a temporary logging directory.
    - Creates a directory before each test.
    - Ensures all loggers and handlers are closed after the test.
    - Deletes the directory and files after the test.
    """
    log_dir = Path("temp_logs")
    log_dir.mkdir(exist_ok=True)
    yield log_dir

    # Ensure all loggers and their handlers are closed
    for logger in logging.Logger.manager.loggerDict.values():
        if isinstance(logger, logging.Logger):
            for handler in logger.handlers[:]:
                logger.removeHandler(handler)
                handler.close()

    # Remove log files and directory
    for log_file in log_dir.glob("*.log"):
        log_file.unlink()
    log_dir.rmdir()


class TestLoggingFunctions:
    """Class to group all logging-related test cases."""

    class TestSetupLogger:
        """
        Test suite for the `setup_logger` function.
        """

        def test_creates_log_file(self, temp_log_dir):
            """Test if `setup_logger` creates a log file and writes log messages."""
            log_file = temp_log_dir / "test_logger.log"
            logger = setup_logger("test_logger", log_file)
            logger.info("This is a test log message.")
            assert log_file.exists()
            with open(log_file, "r") as f:
                logs = f.read()
            assert "This is a test log message." in logs

        def test_uses_correct_format(self, temp_log_dir):
            """Test if `setup_logger` uses the specified format."""
            log_file = temp_log_dir / "formatted_logger.log"
            log_format = "%(asctime)s - %(levelname)s - %(message)s"
            logger = setup_logger(
                "formatted_logger", log_file, logging_format=log_format
            )
            logger.warning("Warning message.")
            with open(log_file, "r") as f:
                logs = f.read()
            assert " - WARNING - Warning message." in logs

        def test_handles_invalid_path(self):
            """Test if `setup_logger` raises an error for an invalid file path."""
            invalid_log_file = Path("/invalid_path/test_logger.log")
            with pytest.raises(Exception):
                setup_logger("test_logger", invalid_log_file)

        def test_concurrent_logging(self, temp_log_dir):
            """Test if multiple loggers can write to their respective files concurrently."""
            log_file1 = temp_log_dir / "logger1.log"
            log_file2 = temp_log_dir / "logger2.log"

            logger1 = setup_logger("logger1", log_file1)
            logger2 = setup_logger("logger2", log_file2)

            # Log messages from two different loggers
            logger1.info("Logger1 message.")
            logger2.info("Logger2 message.")

            # Check both log files for respective messages
            assert log_file1.exists()
            assert log_file2.exists()

            with open(log_file1, "r") as f1, open(log_file2, "r") as f2:
                logs1 = f1.read()
                logs2 = f2.read()

            assert "Logger1 message." in logs1
            assert "Logger2 message." in logs2

    class TestFindValidLogger:
        """
        Test suite for the `find_valid_logger` function.
        """

        def test_creates_failover_logger(self, temp_log_dir):
            """Test if `find_valid_logger` creates a failover logger when the logger doesn't exist."""
            failover_log = temp_log_dir / "Fail_Over - dummy_logger.log"
            logger = find_valid_logger("dummy_logger", default_logging_dir=temp_log_dir)
            logger.error("Failover logger test.")
            assert failover_log.exists()
            with open(failover_log, "r") as f:
                logs = f.read()
            assert "Failover logger test." in logs

        def test_returns_existing_logger(self, temp_log_dir):
            """Test if `find_valid_logger` returns an existing logger."""
            log_file = temp_log_dir / "existing_logger.log"
            existing_logger = setup_logger("existing_logger", log_file)
            existing_logger.info("Existing logger test.")
            logger = find_valid_logger(
                "existing_logger", default_logging_dir=temp_log_dir
            )
            logger.info("Additional log message.")
            with open(log_file, "r") as f:
                logs = f.read()
            assert "Existing logger test." in logs
            assert "Additional log message." in logs
