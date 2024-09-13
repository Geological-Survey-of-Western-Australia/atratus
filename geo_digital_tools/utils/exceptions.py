from typing import Callable
from geo_digital_tools.utils.logging import find_valid_logger


class GeoDigitalError(BaseException):
    """
    These errors are exception classes that log errors instead of breaking the flow of code.

    The Atratus instance of KnownException is to be raised in cases of known issues.

    Known Issue Non-Critical:
    c = function_1(a,b) --> b might be empty but c can still be valid --> log error message regarding b --> still return c
    d = function_2(c) --> function 2 runs as expected

    Known Issue Critical:
    c = function_a(a,b) --> b might be empty but c will be invalid --> log error message regarding b --> stop
    d = function_2(c) --> doesn't run
    ------


    """

    def __init__(super):
        pass


class KnownException(GeoDigitalError):
    def __init__(super, message, level="info", should_raise=False):
        """
        A class to represent KnownExceptions, capturing logging and exception handling.

        ...

        Parameters
        ----------
            message : str
                a message capturing the error.
            level : str
                level to log the error message.
                ["debug", "info", "warning", "error", "critical"]
            should_raise : bool
                if the error should break the flow of code

        """
        # TODO only differnece between these two classes is the destination logger.
        # I can probably refactor these down considerably.

        valid_levels = ["debug", "info", "warning", "error", "critical"]

        warn_flag = False
        if level not in valid_levels:
            warn_flag = True
            level = "critical"

        # check the loggers
        logger_id = "file_issues"
        logger = find_valid_logger(logger_id)

        if level == "debug":
            logger.debug(message)
        if level == "info":
            logger.info(message)
        if level == "warning":
            logger.warning(message)
        if level == "error":
            logger.error(message)
        if level == "critical":
            logger.critical(message)
        if warn_flag:
            logger.critical("Invalid logging level specified defaulting to CRITICAL")
            logger.critical(message)
        if should_raise:
            raise super


class CodeError(GeoDigitalError):
    def __init__(super, message, should_raise=False):
        """
        A class to represent CodeError, capturing and logging to a seperate file.
        These are primarily going to be uncaught exceptions raised via exception_handler decorator.
        However they may also be specific expected failures during development etc.

        ...

        Parameters
        ----------
            message : str
                a message capturing the error.
            level : str
                level to log the error message.
                ["debug", "info", "warning", "error", "critical"]
            should_raise : bool
                if the error should break the flow of code

        """
        # check the loggers
        logger_id = "code_issues"
        logger = find_valid_logger(logger_id)
        logger.critical(message)


        if should_raise:
            raise super


def exception_handler(should_raise=False):
    """
    This function is a pseudo-decorator, for catching and logging unexpected code errors.
    ...

    Parameters
    ----------
        should_raise : bool
            if true raises the 'uncaught' exception

    Examples
    ----------
    Consider a guarnateed KeyError as the dictionary is empty.

    @exception_handler()
    def my_bad_unimportant_function():
        silly = {}
        print(silly['Billy']) --> this will raise a KeyError

    execution
    > my_bad_unimportant_function() --> logs and fails quietly
    > my_other_function() --> this will run


    @exception_handler(should_break=True)
    def my_bad_super_critical_function():
        silly = {}
        print(silly['Billy']) --> this will raise a KeyError

    execution
    > my_bad_super_critical_function() --> logs and slams on the breaks
    > my_other_function() --> this will NOT run

    """

    def wrapper(func: Callable):  # handles the usage of the decorator inputs
        def wrapper_func(*args, **kwargs):  # captures and returns the
            try:
                value = func(*args, **kwargs)
                return value

            except Exception as e:
                CodeError(
                    f"{func.__name__} has encountered uncaught exception {type(e).__name__} with message {str(e)}",
                    should_raise=should_raise,
                )

        return wrapper_func

    return wrapper
