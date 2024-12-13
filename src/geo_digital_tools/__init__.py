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
from geo_digital_tools.database.write import WriteInterface
from geo_digital_tools.database.create_v2 import CreateInterface

from geo_digital_tools.utils.exceptions import KnownException, CodeError

__all__ = [
    "database",
    "utils",
    "ReadInterface",
    "WriteInterface",
    "CreateInterface",
    "KnownException",
    "CodeError",
]
