"""GeoDigitalToolkit

A common toolkit for data handling at GSWA.
"""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("geo_digital_tools")
except PackageNotFoundError:
    pass


from geo_digital_tools import utils
from geo_digital_tools.database import (
    connect,
    create_from_dataframe,
    insert,
    select,
    write_db_metadata_table,
)
from geo_digital_tools.utils.exceptions import (
    CodeError,
    KnownException,
    exception_handler,
)
from geo_digital_tools.utils.logging import setup_logger
from geo_digital_tools.utils.statements import load_statement

__all__ = [
    "utils",
    "connect",
    "create_from_dataframe",
    "insert",
    "select",
    "write_db_metadata_table",
    "CodeError",
    "KnownException",
    "exception_handler",
    "setup_logger",
    "load_statement",
]
