import json
from pathlib import Path
import geo_digital_tools as gdt
import pandas as pd
import sqlalchemy as sqla
from typing import Literal


def connect(
    cfg_path: str | Path, local_db_path=None
) -> tuple[sqla.Engine, sqla.MetaData]:
    """Connect to an engine from a config file.

    e.g. configs/config.json:
    {"sqlalchemy": {"sqlalchemy.url": "sqlite+pysqlite:///:memory:"}}

    Args:
        cfg_path: Path to config file.
        local_db_path: Overwrite the SQLAlchemy URL in config with new path to local file.
    """
    cfg_path = Path(cfg_path)
    if not cfg_path.exists():
        FileNotFoundError(f"{cfg_path.absolute()} not found.")

    with open(cfg_path) as f:
        db_config = json.load(f)
    sqla_cfg = db_config.pop("sqlalchemy")
    if local_db_path:
        sqla_cfg["sqlalchemy.url"] = f"sqlite:///{local_db_path}\\atratus_WAMEX.db"
    try:
        engine = sqla.engine_from_config(configuration=sqla_cfg)
    except sqla.exc.ArgumentError as e:
        gdt.KnownException(
            f"Malformed config file: While parsing {sqla_cfg} encountered {e}",
            should_raise=True,
        )
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


def insert(
    engine: sqla.Engine,
    table_name: str,
    dataframe: pd.DataFrame,
    if_exists: Literal["replace", "fail", "append"] = "replace",
) -> None:
    """Execute an insert statement against a specific engine."""
    try:
        with engine.begin() as connection:
            dataframe.to_sql(
                name=table_name,
                con=connection,
                if_exists=if_exists,
                method=None,
                index=False,
            )
    except Exception as exc:
        raise exc


def write_db_metadata_table(engine: sqla.Engine, cygnet, run_datetime, **metadata):
    """Record runtime metadata to generated database.

    Args:
        engine: SQLAlchemy Engine.
        cygnet: Module containing the codebase of the running code.
        utc_iso_start: Timestamp to record start of script running - preferred ISO UTC.
        **metadata: Additional cygnet specific metadata terms to record against their kwarg name.

    Hint:
        Suggested kwargs to capture as additional metadata include:
            - The geodigital configuration file contents,
            - The select statement that was generated,
            - The walltime of the database building script.
    """
    meta = dict(
        geo_digital_tools=f"{gdt.__name__}@{gdt.__version__}",
        cygnet=f"{cygnet.__name__}@{cygnet.__version__}",
        utc_iso_start=run_datetime,
        **metadata,
    )

    meta_df = pd.DataFrame(meta, index=["Value at runtime:"])
    gdt.insert(engine=engine, table_name="runtime_metadata", dataframe=meta_df)
