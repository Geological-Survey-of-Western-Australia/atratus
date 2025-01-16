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
from geo_digital_tools.utils.statements import load_statement_config, statement_builder
from geo_digital_tools.database import (
    connect,
    select,
    insert,
    create_from_dataframe,
)

from geo_digital_tools.utils.exceptions import (
    CodeError,
    KnownException,
    exception_handler,
)

from geo_digital_tools.utils.logging import setup_logger

__all__ = [
    "load_statement_config",
    "setup_logger",
    "statement_builder",
    "utils",
    "connect",
    "create_from_dataframe",
    "select",
    "insert",
    "KnownException",
    "CodeError",
    "exception_handler",
]
