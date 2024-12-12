import pandas as pd
import sqlalchemy as sqla

import geo_digital_tools.utils.exceptions as gde


class ReadInterface:
    """
    This class acts as a the base class for all of the interfaces our other projects will inherit from.
    """

    def __init__(self, engine: sqla.Engine):
        # may wish to consider using pydantic to enforce strict typing
        self.engine = engine
        self.statement = self.select_statement()
        # only ever set this to true by using the validate interface function
        self.valid = False
        self.result: list = []

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
