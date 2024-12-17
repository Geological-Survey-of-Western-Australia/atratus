import pandas as pd
import sqlalchemy as sqla

from geo_digital_tools.utils.exceptions import GeoDigitalError, KnownException


class ReadInterface:
    """
    This class acts as a the base class for all of the interfaces our other projects will inherit from.
    """

    def __init__(self, engine: sqla.Engine):
        # may wish to consider using pydantic to enforce strict typing
        self.engine = engine
        self.statement = self.select_statement()
        # only ever set this to true by using the validate interface function
        self._valid = False
        self.result: list = []

    def select_statement(self) -> sqla.Select:
        """
        This method should be over written by other modules.
        """

        return sqla.Select()

    def validate_interface(self):
        """Apply a series of checks to the Read statement"""
        if not isinstance(self.statement, sqla.Select):
            KnownException(
                "Interface : Statement is not a Select; ReadInterface requires a select statement",
                should_raise=True,
            )

        # check statement returns values from engine
        try:
            with self.engine.begin() as conn:
                get_one = self.statement.limit(1)
                check_result = conn.execute(get_one)
        except Exception as exc:
            GeoDigitalError(f"Interface : Unhandled Exception {exc}")

        if check_result is not None:
            self._valid = True
            # self.get_interface()
        else:
            KnownException("Interface : Returned no values")

    def query_interface(self):
        if self._valid:
            # create connection
            with self.engine.begin() as conn:
                for row in conn.execute(self.statement):
                    row_as_dict = row._mapping
                    self.result.append(row_as_dict)
        else:
            KnownException("Read statement is not valid", should_raise=True)

    def query_to_df(self):
        """Create a dataframe from a prepared query result"""
        return pd.DataFrame(self.result)

    def df_from_interface(self):
        """Create a dataframe directly from an executed query statement"""
        if self._valid:
            with self.engine.begin() as conn:
                result = conn.execute(self.statement)
                df = pd.DataFrame(result.all(), columns=result.keys())
            return df
        else:
            KnownException("Read statement is not valid", should_raise=True)
