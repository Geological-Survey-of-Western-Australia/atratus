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
    engine = sqla.engine_from_config(configuration=sqla_cfg)
    meta_data = sqla.MetaData()
    return (engine, meta_data)


def create_from_sqla(metadata):
    """"""
    sqla.Table("table_name", metadata, sqla.Column("column_name", sqla.String))


def create_from_data(
    engine: sqla.Engine,
    metadata: sqla.MetaData,
    data: str | Path | pd.DataFrame,
    table_name: str | None = None,
    schema_name: str | None = None,
) -> None:
    """Create tables and columns in a database.
    Table definition can be inferred from example data
    """

    if isinstance(data, pd.DataFrame):
        name = table_name if isinstance(table_name, str) else "unnamed"
    if isinstance(data, (str, Path)):
        data_path = Path(data)
        name = table_name if isinstance(table_name, str) else data_path.stem
        data = pd.read_csv(data_path, header="infer")
    # NOTE we might want the schema to be linked to cygnet name eg geodigitaldatabase.skippy.table1
    # schema_name = ''
    try:
        with engine.begin() as connection:
            data.to_sql(name=name, con=connection, index=False)  # schema=schema_name
    # TODO we'll be populating this area will all the possible gdt.KnownExceptions
    except Exception as exc:
        pass

    metadata.create_all(bind=engine)


def select(engine: sqla.Engine, statement) -> pd.DataFrame:
    """Execute a select statement against a specific engine, returning a Dataframe."""
    try:
        with engine.begin() as conn:
            result = conn.execute(statement).all()
        df = pd.DataFrame(result)
    except Exception as exc:
        pass

    return df


def insert(engine: sqla.Engine, table_name: str, dataframe: pd.DataFrame) -> None:
    """Execute an insert statement against a specific engine."""
    try:
        with engine.begin() as connection:
            dataframe.to_sql(
                table_name, connection, if_exists="fail", method="multi", index=False
            )
    except Exception as exc:
        pass
