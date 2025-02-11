"""Exceptions specific to geo digital tools.

These exceptions are useful in directing information to specific log files.
"""


class GeoDigitalException(Exception):
    """GeoDigitalError exists as a category of Exceptions bespoke to geodigitaltools."""

    pass


class KnownException(GeoDigitalException):
    """Raised when a Cygnet encounters an issue with data being processed."""

    pass


class CodeError(GeoDigitalException):
    """Raised when a Cygnet encounters an issue with code used to process data."""

    pass
