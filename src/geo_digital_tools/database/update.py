# import sqlalchemy as sqla
# import pandas as pd

# import geo_digital_tools.utils.exceptions as gde

# class WriteInterface:
#     """
#     This class acts as a the base class for all of the interfaces our other projects will inherit from.
#     """

#     def __init__(self, engine: sqla.engine):
#         # may wish to consider using pydantic to enforce strict typing
#         self.engine = engine
#         self.statement = self.select_statement()
#         # only ever set this to true by using the validate interface function
#         self.valid = False
#         self.result = []

#     def select_statement(self) -> sqla.Select:
#         """
#         This method should be over written by other modules.
#         """

#         return sqla.Select()

#     def validate_interface(self, input : pd.DataFrame):
#         # check if valid statement for engine
#         insert_statement = isinstance(self.statement, sqla.Insert)
#         if not insert_statement:
#             gde.KnownException(
#                 "Interface : Statement not Insert Write Interface Requires Insert Statement"
#             )

#         # check if returns values
#         source_dest_columns_match = False
#         # NOTE df colums and statement columns should match
#         if source_dest_columns_match:
#             gde.KnownException("Interface : Source and Desintation columns don't match")

#         if insert_statement and not source_dest_columns_match:
#             self.valid = True
#             self.insert_to_interface(input)

#     def insert_to_interface(self):
#         if self.valid:
#             input.to_sql(table_name, self.engine)

#     def df_to_interface(self, input : pd.Dataframe):
#         self.validate_interface()
#         self.insert_to_interface()
#         return pd.DataFrame(self.result)
