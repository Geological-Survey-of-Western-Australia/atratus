"""Abstraction for database operations using SQLAlchemy"""

import sqlalchemy as _sqla

from geo_digital_tools.database.utils import (
    METADATA,
    get_tables_names,
    interface_to_csv,
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
    "BigInteger": _sqla.BigInteger,
    "Boolean": _sqla.Boolean,
    "DateTime": _sqla.DateTime,
    "Double": _sqla.Double,
    "Enum": _sqla.Enum,
    "Float": _sqla.Float,
    "Integer": _sqla.Integer,
    "LargeBinary": _sqla.LargeBinary,
    "Numeric": _sqla.Numeric,
    "PickleType": _sqla.PickleType,
    "String": _sqla.String,
    "Text": _sqla.Text,
    "UnicodeText": _sqla.UnicodeText,
    "Uuid": _sqla.Uuid,
}


__all__ = [
    "METADATA",
    "SUPPORTED_TYPES",
    "get_tables_names",
    "tables_from_config",
    "get_table",
    "interface_to_csv",
]
