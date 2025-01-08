import json
from pathlib import Path

import sqlalchemy as sqla
import pandas as pd


def connect(cfg_path: str | Path) -> sqla.Engine:
    """Connect to an engine from a config file.

    e.g. configs/config.json:
    {"sqlalchemy": {"sqlalchemy.url": "sqlite+pysqlite:///:memory:"}}
    """
    cfg_path = Path(cfg_path)
    if not cfg_path.exists():
        FileNotFoundError(f"{cfg_path.absolute()} not found.")

    with open(cfg_path) as f:
        db_config = json.load(f)
    sqla_cfg = db_config.pop("sqlalchemy")

    return sqla.engine_from_config(configuration=sqla_cfg)


def create_from_sqla(metadata):
    """"""
    sqla.Table("table_name", metadata, sqla.Column("column_name", sqla.String))


def create_from_data(
    engine: sqla.Engine, metadata: sqla.MetaData, data_path: str | Path
) -> None:
    """Create tables and columns in a database.
    Table definition can be inferred from example data
    """
    try:
        data_path = Path(data_path)
        data = pd.read_csv(data_path, header="infer")
        data.to_sql(name=data_path.name, con=engine)

    except Exception as exc:
        pass
    metadata.create_all()


def select(engine: sqla.Engine, statement) -> pd.DataFrame:
    """Execute a select statement against a specific engine, returning a Dataframe."""
    try:
        with engine.begin() as conn:
            result = conn.execute(statement)
        df = pd.DataFrame(result.all(), columns=result.keys())
    except Exception as exc:
        pass

    return df


def insert(engine: sqla.Engine, table_name: str, dataframe: pd.DataFrame) -> None:
    """Execute an insert statement against a specific engine."""
    try:
        dataframe.to_sql(table_name, engine, if_exists="fail", method="multi")
    except Exception as exc:
        pass
