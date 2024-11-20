import json
from pathlib import Path
import sqlalchemy as sqla

from geo_digital_tools.database import connect
import geo_digital_tools.utils.exceptions as gdte


class ColumnBuilder:
    """
    Note that for the most part we should use the CamelCase Classes as they are database Agnostic.
    https://docs.sqlalchemy.org/en/20/core/type_basics.html#the-camelcase-datatypes

    Down the line if we opt to support other SQL tyes (such as ARRAY).
    We will need to consider a method for each flavour of SQL.

    I've selectively removed some supported camelcase types typically to reduce complext.
    Consider the case of date, SqlAlchemy supportes, Date, Time, and DateTime.
    My preference is to force a full date time wherever possible (even if we end up with a number of entries at midnight ;).

    #TODO should work out what to do if the config fails for a given column, do we skip it and the related load? or fail build?
    """

    def __init__(self, columns_json: dict = {}):
        self.columns_json = columns_json
        self.supported_types = {
            "BigInteger": sqla.BigInteger,
            "Boolean": sqla.Boolean,
            "DateTime": sqla.DateTime,
            "Double": sqla.Double,
            "Enum": sqla.Enum,
            "Float": sqla.Float,
            "Integer": sqla.Integer,
            "LargeBinary": sqla.LargeBinary,
            "Numeric": sqla.Numeric,
            "PickleType": sqla.PickleType,
            "String": sqla.String,
            "Text": sqla.Text,
            "UnicodeText": sqla.UnicodeText,
            "Uuid": sqla.Uuid,
        }

        self.failed_columns = {}
        self.validate_columns()
        self.columns = self.build()

    def validate_columns(self):
        column_names = self.columns_json.keys()
        # duplicate keys detected
        if len(column_names) != len(set(column_names)):
            gdte.KnownException(
                f"Column Builder - Unsupported Type : Column - {column_name} Type {column_var}"
            )
        # column unsupported vartype
        for column_name, column_var in self.columns_json.items():
            if column_var not in list(self.supported_types.keys()):
                gdte.KnownException(
                    f"Column Builder - Unsupported Type : Column - {column_name} Type {column_var}",
                    should_raise=True,
                )
                self.failed_columns[column_name] = column_var

    def build(self) -> tuple[sqla.Column]:
        cols = []
        for column_name, column_var in self.columns_json.items():
            if column_var not in list(self.supported_types.keys()):
                gdte.KnownException(
                    f"Column Builder - Unsupported Type : Column - {column_name} Type {column_var}"
                )
            else:
                cols.append(sqla.Column(column_name, self.supported_types[column_var]))

        return tuple(cols)


def tables_from_config(config: dict, engine: sqla.Engine, meta: sqla.MetaData):

    for table_name, columns_json in config.items():
        columns = ColumnBuilder(columns_json=columns_json).columns
        table = sqla.Table(table_name, meta, *columns)

    # create all the tables in the associated db
    meta.create_all(engine)


def dict_raise_on_duplicates(ordered_pairs):
    """Reject duplicate keys, this should be modified to reflect nested json objects
    FIXME
    example_config = {
        table1 : {col1:str,col2:int,col1:datetime} <- second col1 overwritest the first
        table1 : {col_1:datetime,col_2:int,col_1:str} <- would overwrite the first table
    }

    """
    d = {}
    for k, v in ordered_pairs:
        if k in d:
            gdte.KnownException(
                f"GDT - Duplicate Keys detected in Databse Config : {k}",
                should_raise=True,
            )
        else:
            d[k] = v
    return d


def parse_database_config(config_path: Path):

    with open(config_path) as f:
        # NOTE here we're screening for duplicate table names
        config = json.load(f, object_pairs_hook=dict_raise_on_duplicates)

    return config
