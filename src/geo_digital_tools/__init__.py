"""GeoDigitalToolkit

A common toolkit for data handling at GSWA
"""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("geo_digital_tools")
except PackageNotFoundError:
    # package is not installed
    pass


from geo_digital_tools import database, utils
from geo_digital_tools.database.read import ReadInterface

from geo_digital_tools.utils.exceptions import KnownException, CodeError

__all__ = [
    "database",
    "utils",
    "ReadInterface",
    "KnownException",
    "CodeError",
]
