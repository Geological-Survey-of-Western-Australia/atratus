import sqlalchemy as sqla

from geo_digital_tools.utils.exceptions import KnownException, GeoDigitalError


class WriteInterface:
    """Helper class to write to a database"""

    def __init__(self, engine: sqla.Engine):
        self.engine = engine

    def __str__(self):
        """Useful for printing diagnostic information about an interface"""
        return f"{type(self).__name__}, {self.engine.url}"

    def write(self):
        """Overridable method to define how to write to a database"""
        raise NotImplementedError(
            "This method should be overwritten for your application"
        )
