"""Cygnet Database Utilities.

Description:
    A collection of tools for database operations using SQLAlchemy and Pandas.
    Provides functions to connect to databases, create/update tables from schemas or DataFrames,
    execute queries, and manage runtime metadata.

Key Features:
    - Config-driven database connections
    - Schema definition via SQLAlchemy or DataFrame inference
    - Type-safe CRUD operations
    - Runtime metadata tracking
"""

import json
import types
from datetime import datetime
from pathlib import Path
from typing import Any, Literal

import pandas as pd
import sqlalchemy as sqla
from sqlalchemy.sql.expression import Selectable

import geo_digital_tools as gdt


def connect(
    cfg_path: str | Path, local_db_path: str | Path | None = None
) -> tuple[sqla.Engine, sqla.MetaData]:
    """Connect to an engine from a config file.

    For example, configs/config.json might contain:
    {"sqlalchemy": {"sqlalchemy.url": "sqlite+pysqlite:///:memory:"}}

    Args:
        cfg_path (str | Path): Path to the JSON config file.
        local_db_path (str | Path | None, optional):  Overwrite the `sqlalchemy.url` in config with the provided local file path. Defaults to None.

    Returns:
        tuple[sqla.Engine, sqla.MetaData]: SQLAlchemy Engine and MetaData objects.

    Raises:
        FileNotFoundError: If the config file does not exist.
        gdt.KnownException: If the config file is malformed.
    """
    cfg_path = Path(cfg_path)
    if not cfg_path.exists():
        raise FileNotFoundError(f"{cfg_path.absolute()} not found.")

    with open(cfg_path, encoding="utf-8") as f:
        db_config = json.load(f)
    sqla_cfg = db_config.pop("sqlalchemy")

    if local_db_path:
        sqla_cfg["sqlalchemy.url"] = (
            f"sqlite:///{local_db_path}"  # for windows
        )
        # sqla_url = f"sqlite:///{local_db_path}/{atratus_WAMEX.db}" # for linux/macOS
    try:
        engine = sqla.engine_from_config(configuration=sqla_cfg)
    except sqla.exc.ArgumentError as exc:
        raise gdt.KnownException(
            f"Malformed config file: While parsing {sqla_cfg}.",
        ) from exc
    meta_data = sqla.MetaData()
    return (engine, meta_data)


def create_from_sqla(
    engine: sqla.Engine,
    metadata: sqla.MetaData,
    table_name: str,
    column_name: str,
    sqla_dtype: sqla.types.TypeEngine,
) -> None:
    """Define tables and columns in a database from SQLAlchemy function calls.

    Args:
        engine (sqlalchemy.Engine): Database connection engine.
        metadata (sqlalchemy.MetaData): SQLAlchemy MetaData object.
        table_name (str): Name of the table to create or update.
        column_name (str): Name of the column to create or update.
        sqla_dtype (sqlalchemy.types.TypeEngine): SQLAlchemy data type to apply.

    Returns:
        None
    Raises:
        Exception: If table/column definition fails.
    """
    try:
        sqla.Table(
            table_name,
            metadata,
            sqla.Column(column_name, sqla_dtype),
            autoload_with=engine,
        )
    except Exception as exc:
        raise exc


def create_from_dataframe(
    engine: sqla.Engine,
    metadata: sqla.MetaData,
    dataframe: pd.DataFrame,
    table_name: str = "unnamed_table",
    # schema_name: str | None = None,
) -> None:
    """Create tables and columns in a database, inferred from a sample DataFrame.

    Args:
        engine (sqlalchemy.Engine): Database connection engine.
        metadata (sqlalchemy.MetaData): SQLAlchemy MetaData object.
        dataframe (pd.DataFrame): DataFrame with columns used to infer table schema.
        table_name (str, optional): Name of the table to create. Defaults to "unnamed_table".

    Returns:
        None

    Raises:
        Exception: If table creation fails.
    """
    # NOTE we might want the schema to be linked to cygnet name eg geodigitaldatabase.skippy.table1
    try:
        with engine.begin() as connection:
            dataframe.to_sql(name=table_name, con=connection, index=False)
            # schema=schema_name
        metadata.reflect(bind=engine)
    # TODO we'll be populating this area will all the possible gdt.KnownExceptions
    except Exception as exc:
        raise exc

    metadata.create_all(bind=engine)


def select(engine: sqla.Engine, statement: Selectable | str) -> pd.DataFrame:
    """Execute a SELECT statement against a specific engine, returning a DataFrame.

    Args:
        engine (sqlalchemy.Engine): Database connection engine.
        statement (Selectable | str): A SQLAlchemy statement or raw SQL text to execute.

    Returns:
        pd.DataFrame: Results of the SELECT query.

    Raises:
        Exception: If execution or data retrieval fails.
    """
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
    """Execute an INSERT statement against a specific engine.

    Args:
        engine (sqlalchemy.Engine): Database connection engine.
        table_name (str): Name of the target table for insertion.
        dataframe (pd.DataFrame): DataFrame to insert into the table.
        if_exists (Literal["replace", "fail", "append"], optional): Behavior if table
            already exists. Defaults to "replace".

    Returns:
        None

    Raises:
        Exception: If insertion fails.
    """
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


def write_db_metadata_table(
    engine: sqla.Engine,
    cygnet: types.ModuleType,
    run_datetime: str | datetime,
    **metadata: dict[str, Any],
) -> None:
    """Record runtime metadata to generated database.

    Args:
        engine (sqlalchemy.Engine): Database connection engine,SQLAlchemy Engine.
        cygnet (types.ModuleType): A module containing the codebase of the running code,
            expected to have `__name__` and `__version__` attributes.
        run_datetime (str | datetime): Timestamp to record the start of script execution (preferably an ISO UTC string).
        **metadata (dict[str, Any]): Additional metadata to record, using the keyword argument as the metadata field name.

    Hint:
        Suggested kwargs to capture as additional metadata include:
            - The geodigital configuration file contents,
            - The generated SQL `SELECT` statement,
            - The total execution time of the database building script.
    """
    meta = dict(
        geo_digital_tools=f"{gdt.__name__}@{gdt.__version__}",
        cygnet=f"{cygnet.__name__}@{cygnet.__version__}",
        utc_iso_start=(
            run_datetime.isoformat()
            if isinstance(run_datetime, datetime)
            else run_datetime
        ),
        **metadata,
    )

    meta_df = pd.DataFrame(meta, index=["Value at runtime:"])
    gdt.insert(engine=engine, table_name="runtime_metadata", dataframe=meta_df)
