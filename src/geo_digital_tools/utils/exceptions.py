"""Exceptions specific to geo digital tools"""

import functools
from typing import Callable

from geo_digital_tools.utils.logging import find_valid_logger


class GeoDigitalError(Exception):
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
        # TODO only difference between these two classes is the destination logger.
        # I can probably refactor these down considerably.

        valid_levels = ["debug", "info", "warning", "error", "critical"]

        warn_flag = False
        if level not in valid_levels:
            warn_flag = True
            level = "critical"

        # check the loggers
        logger_id = "known_exceptions"
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
            logger.critical("Invalid logging level specified, defaulting to CRITICAL")
            logger.critical(message)
        if should_raise:
            raise super


class CodeError(GeoDigitalError):
    def __init__(super, message):
        """
        A class to represent errors intrinsic to the Python code, capturing and logging
        to a seperate file.
        These are primarily going to be uncaught exceptions raised via the
        exception_handler decorator. However they may also be specific expected
        failures during development etc.

        ...

        Parameters
        ----------
            message : str
                A message capturing the error.
            level : str
                Level to log the error message.
                ["debug", "info", "warning", "error", "critical"]
            should_raise : bool
                If the error should break the flow of code
        """
        # check the loggers
        logger_id = "code_issues"
        logger = find_valid_logger(logger_id)
        logger.critical(message)


def exception_handler(
    CustomException: Exception | None = None,
    should_raise: bool = False,
):
    """
    This function is expected to be used as a decorator,
    for catching and logging:
        - Errors that are "known", and described in the custom exception,
        - and unexpected code errors.
    ...

    Parameters
    ----------
        CustomException: Exception
            If the issue triggers a KnownException and can be explained
        should_raise : bool
            if true raises the 'uncaught issue' CodeError exception

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

    def wrapper(func: Callable):
        @functools.wraps(func)
        def wrapper_func(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as super_exc:
                if CustomException is not None:
                    exc = CustomException
                else:
                    exc = CodeError(f"{func.__name__} encountered {str(super_exc)}.")

                if should_raise:
                    raise exc from super_exc

        return wrapper_func

    return wrapper
