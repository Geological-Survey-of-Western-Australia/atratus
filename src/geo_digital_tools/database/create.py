# import json
# from pathlib import Path
# import sqlalchemy as sqla

# import geo_digital_tools
# from geo_digital_tools import KnownException, exception_handler


# class ColumnBuilder:
#     """
#     Construct tables of specific types from configuration file
#     #TODO should work out what to do if the config fails for a given column, do we skip it and the related load? or fail build?
#     """

#     def __init__(self, columns_json: dict = {}):
#         self.columns_json = columns_json
#         self.supported_types = geo_digital_tools.database.SUPPORTED_TYPES

#         self.failed_columns: dict[str, str] = {}
#         self.validate_columns()
#         self.columns = self.build()

#     def validate_columns(self):
#         column_names = self.columns_json.keys()
#         # duplicate keys detected
#         if len(column_names) != len(set(column_names)):
#             KnownException("Column Builder - Duplicate column names detected")

#         # column unsupported vartype
#         for column_name, column_var in self.columns_json.items():
#             if column_var not in list(self.supported_types.keys()):
#                 KnownException(
#                     f"Column Builder - Unsupported Type : Column - {column_name} Type {column_var}",
#                     should_raise=True,
#                 )
#                 self.failed_columns[column_name] = column_var

#     def build(self) -> tuple[sqla.Column]:
#         cols = []
#         for column_name, column_var in self.columns_json.items():
#             if column_var not in list(self.supported_types.keys()):
#                 KnownException(
#                     f"Column Builder - Unsupported Type : Column - {column_name} Type {column_var}"
#                 )
#             else:
#                 cols.append(sqla.Column(column_name, self.supported_types[column_var]))

#         return tuple(cols)


# def tables_from_config(config: dict, engine: sqla.Engine, meta: sqla.MetaData):
#     """Generate SQL tables based on structure defined in config"""
#     for table_name, columns_json in config.items():
#         columns = ColumnBuilder(columns_json=columns_json).columns
#         table = sqla.Table(table_name, meta, *columns)

#     # create all the tables in the associated db
#     meta.create_all(engine)


# def dict_raise_on_duplicates(ordered_pairs):
#     """Reject duplicate keys, this should be modified to reflect nested json objects
#     FIXME
#     example_config = {
#         table1 : {col1:str,col2:int,col1:datetime} <- second col1 overwrites the first
#         table1 : {col_1:datetime,col_2:int,col_1:str} <- would overwrite the first table
#     }

#     """
#     d = {}
#     for k, v in ordered_pairs:
#         if k in d:
#             KnownException(
#                 f"GDT - Duplicate Keys detected in Databse Config : {k}",
#                 should_raise=True,
#             )
#         else:
#             d[k] = v
#     return d


# def parse_database_config(config_path: Path):
#     """Load JSON config while screening for duplicate table names"""
#     with open(config_path) as f:
#         config = json.load(f, object_pairs_hook=dict_raise_on_duplicates)

#     return config
