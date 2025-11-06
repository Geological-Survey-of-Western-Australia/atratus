"""GSWA - Atratus

A common tools for data handling at GSWA.
"""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("gswa_atratus")
except PackageNotFoundError:
    pass


from gswa_atratus import utils
from gswa_atratus.database import (
    connect,
    create_from_dataframe,
    insert,
    select,
    write_db_metadata_table,
)
from gswa_atratus.utils.exceptions import (
    CodeError,
    KnownException,
)
from gswa_atratus.utils.loggers import use_gdt_logging
from gswa_atratus.utils.statements import load_statement

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
