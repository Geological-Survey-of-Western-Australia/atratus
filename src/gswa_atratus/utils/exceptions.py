"""Exceptions specific to Atratus.

These exceptions are useful in directing information to specific log files.
"""


class AtratusException(Exception):
    """AtratusError exists as a category of Exceptions bespoke to gswa-atratus."""

    pass


class KnownException(AtratusException):
    """Raised when a Cygnet encounters an issue with data being processed."""

    pass


class CodeError(AtratusException):
    """Raised when a Cygnet encounters an issue with code used to process data."""

    pass
