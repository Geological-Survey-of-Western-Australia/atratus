import json
from pathlib import Path

import sqlalchemy as sqla

from geo_digital_tools.database import METADATA, SUPPORTED_TYPES
from geo_digital_tools.database.utils import tables_from_config
from geo_digital_tools.utils.exceptions import KnownException, exception_handler


class CreateInterface:
    """Helper class to create a database"""

    def __init__(
        self,
        url: str | sqla.URL | None = None,
        cfg_path: str | Path | None = None,
    ):
        self._fallback: bool = False
        if cfg_path is not None:
            self.from_config(cfg_path)
        elif url is not None:
            self.engine = sqla.create_engine(url=url)
        else:
            KnownException("No engine URL was specified, using in-memory fall-back.")
            self._fallback = True
            self.engine = sqla.create_engine(
                url="sqlite+pysqlite:///:memory:",
                echo="debug",
            )

    @exception_handler(should_raise=True)
    def from_config(self, cfg_path: str | Path):
        """Define an engine and database schema using config file

        Template for config.json:
        {
            "sqlalchemy": {"sqlalchemy.url": "sqlite+pysqlite:///:memory:"},
            "tables": {
                "table1": {
                    "col1": "String",
                    "col2": "String"
                },
                "table2": {
                    "col1": "String"
                }
            }
        }
        """
        cfg_path = Path(cfg_path)
        if not cfg_path.exists():
            FileNotFoundError(f"{cfg_path.absolute()} not found.")

        with open(cfg_path) as f:
            db_config = json.load(f)

        sqla_cfg = db_config.pop("sqlalchemy")

        self.engine = sqla.engine_from_config(configuration=sqla_cfg)

        tables_from_config(db_config)

    def define_db(self):
        """Overridable method in which a database is defined"""
        raise NotImplementedError(
            "This method should be overwritten for your application"
        )

    def validate(self):
        pass

    def create_metadata(self):
        """Create objects in module level metadata store"""
        METADATA.create_all(self.engine)
