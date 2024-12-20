import sqlalchemy as sqla

from geo_digital_tools.utils.exceptions import KnownException, GeoDigitalError


class WriteInterface:
    """The base class for all Write interfaces other projects inherit from."""

    def __init__(self, engine: sqla.Engine):
        self.engine = engine

    def __str__(self):
        """Useful for printing diagnostic information about an interface."""
        return f"{type(self).__name__}, {self.engine.url}"

    def write(self):
        """Replace with an sqlalchemy.Insert statement bespoke to your database."""
        raise NotImplementedError(
            "This method should be overwritten for your application."
        )

    def validate_interface(self):
        """Apply a series of checks to the Write statement."""
        if not isinstance(self.statement, sqla.Insert):
            KnownException(
                "Interface : Statement is not a Insert; WriteInterface requires an insert statement.",
                should_raise=True,
            )

        # TODO: Validate statement is writable to test engine? That seems tricky.
