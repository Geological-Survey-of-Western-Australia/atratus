"""Abstraction for database operations using SQLAlchemy"""

import sqlalchemy

from geo_digital_tools.database.connect import (
    SQLAConnection,
    load_db_config,
    remote_database,
    validate_db_config,
)
from geo_digital_tools.database.utils import (
    METADATA,
    get_tables_names,
    tables_from_config,
)

## GDI supports a subset of valid SQLA data types for compatability
# Note that for the most part we should use the CamelCase Classes as they are database Agnostic.
# https://docs.sqlalchemy.org/en/20/core/type_basics.html#the-camelcase-datatypes

# Down the line if we opt to support other SQL tyes (such as ARRAY).
# We will need to consider a method for each flavour of SQL.

# I've selectively removed some supported camelcase types typically to reduce complexity.
# Consider the case of date, SqlAlchemy supportes, Date, Time, and DateTime.
# My preference is to force a full date time wherever possible (even if we end up with a number of entries at midnight ;).
SUPPORTED_TYPES = {
    "BigInteger": sqlalchemy.BigInteger,
    "Boolean": sqlalchemy.Boolean,
    "DateTime": sqlalchemy.DateTime,
    "Double": sqlalchemy.Double,
    "Enum": sqlalchemy.Enum,
    "Float": sqlalchemy.Float,
    "Integer": sqlalchemy.Integer,
    "LargeBinary": sqlalchemy.LargeBinary,
    "Numeric": sqlalchemy.Numeric,
    "PickleType": sqlalchemy.PickleType,
    "String": sqlalchemy.String,
    "Text": sqlalchemy.Text,
    "UnicodeText": sqlalchemy.UnicodeText,
    "Uuid": sqlalchemy.Uuid,
}


__all__ = [
    "METADATA",
    "SUPPORTED_TYPES",
    "SQLAConnection",
    "load_db_config",
    "validate_db_config",
    "remote_database",
    "ColumnBuilder",
    "get_tables_names",
    "tables_from_config",
]
