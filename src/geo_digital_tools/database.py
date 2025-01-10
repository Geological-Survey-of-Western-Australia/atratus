import json
from pathlib import Path

import pandas as pd
import sqlalchemy as sqla


def connect(cfg_path: str | Path) -> tuple[sqla.Engine, sqla.MetaData]:
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


def create_from_sqla(
    engine: sqla.Engine,
    metadata: sqla.MetaData,
    table_name: str,
    column_name: str,
    sqla_dtype: sqla.types.TypeDecorator,
) -> None:
    """An example function to define Tables and Columns from sqlalchemy function calls."""
    sqla.Table(
        table_name,
        metadata,
        sqla.Column(column_name, sqla_dtype),
        autoload_with=engine,
    )


def create_from_dataframe(
    engine: sqla.Engine,
    metadata: sqla.MetaData,
    dataframe: pd.DataFrame,
    table_name: str = "unnamed_table",
    schema_name: str | None = None,
) -> None:
    """Create tables and columns in a database inferred an example DataFrame."""
    # NOTE we might want the schema to be linked to cygnet name eg geodigitaldatabase.skippy.table1
    # schema_name = ''
    try:
        with engine.begin() as connection:
            dataframe.to_sql(name=table_name, con=connection, index=False)
            # schema=schema_name
    # TODO we'll be populating this area will all the possible gdt.KnownExceptions
    except Exception as exc:
        raise exc

    metadata.create_all(bind=engine)


def select(engine: sqla.Engine, statement) -> pd.DataFrame:
    """Execute a select statement against a specific engine, returning a Dataframe."""
    try:
        with engine.begin() as conn:
            result = conn.execute(statement).all()
        df = pd.DataFrame(result)
    except Exception as exc:
        raise exc

    return df


def insert(engine: sqla.Engine, table_name: str, dataframe: pd.DataFrame) -> None:
    """Execute an insert statement against a specific engine."""
    try:
        with engine.begin() as connection:
            dataframe.to_sql(
                name=table_name,
                con=connection,
                if_exists="fail",
                method="multi",
                index=False,
            )
    except Exception as exc:
        raise exc
