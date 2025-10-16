"""GeoDigitalTools

A common tools for data handling at GSWA.
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
)
from geo_digital_tools.utils.loggers import use_gdt_logging
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
    "use_gdt_logging",
    "load_statement",
]
