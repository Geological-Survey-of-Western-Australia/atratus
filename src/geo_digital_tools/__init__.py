"""GeoDigitalToolkit

A common toolkit for data handling at GSWA
"""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("geo_digital_tools")
except PackageNotFoundError:
    # package is not installed
    pass


from geo_digital_tools import utils
from geo_digital_tools.database import (
    connect,
    create_from_data,
    create_from_sqla,
    select,
    insert,
)

from geo_digital_tools.utils.exceptions import (
    CodeError,
    KnownException,
    exception_handler,
)

__all__ = [
    "utils",
    "connect",
    "create_from_data",
    "create_from_sqla",
    "select",
    "insert",
    "KnownException",
    "CodeError",
    "exception_handler",
]
