import json
from pathlib import Path

import sqlalchemy as sqla

import geo_digital_tools
from geo_digital_tools.utils.exceptions import KnownException, exception_handler

# Global metadata store within GDI
# See https://docs.sqlalchemy.org/en/20/tutorial/metadata.html
METADATA = sqla.MetaData()


def save_to_disk(self, output_path: str | Path = "fallback.db"):
    Path(output_path)
    # pandas df from db? sql db?
    return output_path


def tables_from_config(configuration: dict):
    """Generate SQL table schema based on structure defined in config.
    Table schema is stored in the sessions metadata.

    configuration: A dictionary (typically produced from a config file,

    """
    tables = configuration.pop("tables")

    for table_name, columns_json in tables.items():
        columns = ColumnBuilder(columns_json=columns_json).columns
        sqla.Table(table_name, METADATA, *columns)


def check_valid_sqlite(query_list: list[str]) -> list[str]:
    """Temp location of useful SQL comment checking"""
    select_queries = []
    create_queries = []
    for query in query_list:
        if "--" in str(query):  #  -- is a comment marker in SQL
            query = [command for command in query.split(",") if "--" not in command]
            query = ", ".join(query)
        if "select" in str(query).lower():
            select_queries.append(query)
        if "create" in str(query).lower():
            create_queries.append(query)

    valid_select = check_valid_select(select_queries)
    valid_create = check_valid_create(create_queries)

    # some atttempt to preserve order incase it's important
    valid_queries = [q for q in query_list if q in valid_select or q in valid_create]

    return valid_queries


def get_tables_names(engine: sqla.Engine) -> list[str]:
    """
    This just loads the existing table names and runs faster than meta-data reflect.
    It does not load schemas.
    """
    list_of_tables = []

    try:
        inspector = sqla.inspect(engine)
        list_of_tables = inspector.get_table_names()
    except Exception as e:
        KnownException(
            f"GDT - Found ecountered exception {e} when getting table names."
        )

    if len(list_of_tables) == 0:
        KnownException("GDT - Found no tables in engine.")

    return list_of_tables


def get_table(
    engine: sqla.Engine,
    target_table: str,
    return_schema_as_dict=False,
) -> sqla.Table | None | dict:
    """
    Gets an sqla table from the engine.
    If table name in engines tables returns table.
    Else logs and returns None
    NOTE should this be pulled out into two functions?
    """

    tables = get_tables_names(engine)

    if target_table not in tables:
        KnownException(f"Table {target_table} not found in engine. Skipping.")
        return None
    else:
        TargetTable = sqla.Table(target_table, METADATA, autoload_with=engine)

        if return_schema_as_dict:
            schema_as_dict = {k: str(v.type) for k, v in TargetTable.columns.items()}
            return schema_as_dict

        else:
            return TargetTable


class ColumnBuilder:
    """
    Construct tables of specific types from configuration file
    #TODO should work out what to do if the config fails for a given column, do we skip it and the related load? or fail build?
    """

    def __init__(self, columns_json: dict = {}):
        self.columns_json = columns_json
        self.supported_types = geo_digital_tools.database.SUPPORTED_TYPES

        self.failed_columns: dict[str, str] = {}
        self.validate_columns()
        self.columns = self.build()

    def validate_columns(self):
        column_names = self.columns_json.keys()
        # duplicate keys detected
        if len(column_names) != len(set(column_names)):
            KnownException("Column Builder - Duplicate column names detected")

        # column unsupported vartype
        for column_name, column_var in self.columns_json.items():
            if column_var not in list(self.supported_types.keys()):
                KnownException(
                    f"Column Builder - Unsupported Type : Column - {column_name} Type {column_var}",
                    should_raise=True,
                )
                self.failed_columns[column_name] = column_var

    def build(self) -> tuple[sqla.Column]:
        cols = []
        for column_name, column_var in self.columns_json.items():
            if column_var not in list(self.supported_types.keys()):
                KnownException(
                    f"Column Builder - Unsupported Type : Column - {column_name} Type {column_var}"
                )
            else:
                cols.append(sqla.Column(column_name, self.supported_types[column_var]))

        return tuple(cols)


def dict_raise_on_duplicates(ordered_pairs):
    """Reject duplicate keys, this should be modified to reflect nested json objects
    FIXME
    example_config = {
        table1 : {col1:str,col2:int,col1:datetime} <- second col1 overwrites the first
        table1 : {col_1:datetime,col_2:int,col_1:str} <- would overwrite the first table
    }

    """
    d = {}
    for k, v in ordered_pairs:
        if k in d:
            KnownException(
                f"GDT - Duplicate Keys detected in Databse Config : {k}",
                should_raise=True,
            )
        else:
            d[k] = v
    return d


def parse_database_config(config_path: Path):
    """Load JSON config while screening for duplicate table names"""
    with open(config_path) as f:
        config = json.load(f, object_pairs_hook=dict_raise_on_duplicates)

    return config
