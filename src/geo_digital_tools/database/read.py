import pandas as pd
import sqlalchemy as sqla

import geo_digital_tools.utils.exceptions as gde


class ReadInterface:
    """
    This class acts as a the base class for all of the interfaces our other projects will inherit from.
    """

    def __init__(self, engine: sqla.engine):
        # may wish to consider using pydantic to enforce strict typing
        self.engine = engine
        self.statement = self.select_statement()
        # only ever set this to true by using the validate interface function
        self.valid = False
        self.result = []

    def select_statement(self) -> sqla.Select:
        """
        This method should be over written by other modules.
        """

        return sqla.Select()

    def validate_interface(self):
        # check if valid statement for engine
        select_statement = isinstance(self.statement, sqla.Select)
        if not select_statement:
            gde.KnownException(
                "Interface : Statement not select read interface requires select statement",
                should_raise=True,
            )

        # check if returns values
        statement_returns_none = False
        try:
            conn = self.engine.connect()
            get_one = self.statement.limit(1)
            statement_returns_none = conn.execute(get_one) is None

        except Exception as e:
            gde.GeoDigitalError(f"Interface : Unhandled Excepetion {e}")

        if statement_returns_none:
            gde.KnownException("Interface : Returned no Values")

        if select_statement and not statement_returns_none:
            self.valid = True
            self.get_interface()

    def get_interface(self):
        if self.valid:
            # create connection
            conn = self.engine.connect()
            for row in conn.execute(self.statement):
                row_as_dict = row._mapping
                self.result.append(row_as_dict)
            # close connection
            conn.close()

    def interface_to_df(self):
        return pd.DataFrame(self.result)


def get_tables_names(engine: sqla.Engine) -> list[str]:
    """
    This just loads the existing table names and runs faster than meta-data reflect.
    It does not load schemas.
    """
    list_of_tables = []

    try:
        inspector = sqla.engine.reflection.Inspector.from_engine(engine)
        list_of_tables = inspector.get_table_names()
    except Exception as e:
        gde.KnownException(
            f"GDT - Found ecountered exception {e} when getting table names."
        )

    if len(list_of_tables) == 0:
        gde.KnownException("GDT - Found no tables in engine.")

    return list_of_tables


def get_table(
    engine: sqla.Engine, target_table: str, return_schema_as_dict=False
) -> sqla.Table | None | dict:
    """
    Gets an sqla table from the engine.
    If table name in engines tables returns table.
    Else logs and returns None
    NOTE should this be pulled out into two functions?
    """

    tables = get_tables_names(engine)

    if target_table not in tables:
        gde.KnownException(f"Table {target_table} not found in engine. Skipping.")
        return None
    else:
        meta_data = sqla.MetaData()
        TargetTable = sqla.Table(target_table, meta_data, autoload_with=engine)

        if return_schema_as_dict:
            schema_as_dict = {k: str(v.type) for k, v in TargetTable.columns.items()}
            return schema_as_dict

        elif not return_schema_as_dict:
            return TargetTable
