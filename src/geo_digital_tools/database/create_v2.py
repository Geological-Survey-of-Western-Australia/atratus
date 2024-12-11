import typing

import sqlalchemy as sqla
from sqlalchemy import Column, Integer, MetaData, String, Table

from geo_digital_tools.utils.exceptions import KnownException
from geo_digital_tools.database import METADATA


class CreateInterface:
    """Helper class to create to a database"""

    def __init__(self, engine: sqla.Engine | None = None):
        # if engine is None:
        KnownException("No engine was specified, using in-memory fall-back.")
        self._fallback = True
        self.engine = sqla.create_engine(
            url="sqlite+pysqlite:///:memory:",
            echo="debug",
        )
        # else:
        #     self._fallback = False
        #     self.engine = engine

    def define_db(self):
        """Overridable method in which a database is defined"""
        raise NotImplementedError(
            "This method should be overwritten for your application"
        )

    def create_metadata(self):
        """Create objects in module level metadata store"""
        METADATA.create_all(self.engine)

    def execute(self):
        """Execute the engine with sqla"""
        with self.engine.begin() as conn:
            result = conn.execute()

        return result


if __name__ == "__main__":
    # TODO Move this to atratus
    class AtratusLocalInterface(CreateInterface):
        """In-memory database to store Atratus extracts"""

        def __init__(self, engine=None):
            super().__init__(self)

        @typing.override
        def define_db(self):
            r"""sql
            CREATE TABLE IF NOT EXISTS files (
                ANumber varchar(255),
                file_path varchar(2000),
                file_name varchar(255),
                file_type varchar(255),
                file_hash varchar(255),
                file_year TEXT,
                file_size int
                );

            CREATE TABLE IF NOT EXISTS reports (
                ANumber varchar(255),
                KeywordList varchar(2000),
                TargetCommodityList varchar(2000),
                centroid varchar(2000),
                ReportDate TEXT,
                CONFIDENTIALITY varchar(255)
                );"""

            files = Table(
                "files",
                METADATA,
                Column("ANumber", String, primary_key=True),
                Column("file_path", String),
                Column("file_name", String),
                Column("file_type", String),
                Column("file_hash", String),
                Column("file_year", String),
                Column("file_size", Integer),
            )

            reports = Table(
                "reports",
                METADATA,
                Column(
                    "ANumber", String, primary_key=True
                ),  # sqla.ForeignKey("files.ANumber")
                Column("KeywordList", String),
                Column("TargetCommodityList", String),
                Column("centroid", String),
                Column("ReportDate", String),
                Column("CONFIDENTIALITY", String),
            )

    al = AtratusLocalInterface()
    al.define_db()
    al.create_metadata()
