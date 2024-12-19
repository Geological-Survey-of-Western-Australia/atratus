import pandas as pd
import sqlalchemy as sqla

from geo_digital_tools.utils.exceptions import CodeError, KnownException


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

    def __str__(self):
        """Useful for printing diagnostic information about an interface"""
        return f"{type(self).__name__}, {self.engine.url}"

    def select_statement(self) -> sqla.Select:
        """Replace with an sqlalchemy.Select() statement bespoke to your database.
        https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#using-select-statements
        """
        raise NotImplementedError(
            "This method should be overwritten for your application"
        )

    def validate_interface(self):
        """Apply a series of checks to the Read statement"""
        if not isinstance(self.statement, sqla.Select):
            KnownException(
                f"{type(self).__name__}) : ReadInterface requires a select statement",
                should_raise=True,
            )

        # check statement returns values from engine
        try:
            with self.engine.begin() as conn:
                get_one = self.statement.limit(1)
                check_result = conn.execute(get_one)
        except Exception as exc:
            CodeError(f"{type(self).__name__}) : Unhandled Exception {exc}")

        if check_result is not None:
            self._valid = True
            # self.get_interface()
        else:
            KnownException(f"{type(self).__name__}) : Returned no values")

    def query_interface(self):
        if self._valid:
            # create connection
            with self.engine.begin() as conn:
                for row in conn.execute(self.statement):
                    row_as_dict = row._mapping
                    self.result.append(row_as_dict)
        else:
            KnownException("Read statement is not valid", should_raise=True)

    def query_to_df(self) -> pd.DataFrame:
        """Create a dataframe from a prepared query result"""
        return pd.DataFrame(self.result)

    def df_from_interface(self) -> pd.DataFrame:
        """Create a dataframe directly from an executed query statement"""
        if self._valid:
            with self.engine.begin() as conn:
                result = conn.execute(self.statement)
                df = pd.DataFrame(result.all(), columns=result.keys())
        else:
            KnownException("Read statement has not been validated", should_raise=True)

        return df
