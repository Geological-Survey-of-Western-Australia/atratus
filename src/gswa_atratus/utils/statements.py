"""This module loads and builds SQLAlchemy Select statements from a JSON configuration file.

It uses gswa-atratus (gdt) for custom exception handling and leverages SQLAlchemy's engine,
metadata, and table objects to construct query statements dynamically based on the provided JSON.
"""

import json
from pathlib import Path
from typing import Any

import sqlalchemy as sqla
from sqlalchemy import exc as sqlae
from sqlalchemy.orm import aliased

import gswa_atratus as gdt


def load_statement(
    cfg_path: Path | str, engine: sqla.Engine, metadata: sqla.MetaData
) -> sqla.Select:
    """Load and build a SQLAlchemy Select statement from a gswa-atratus config file.

    Args:
        cfg_path (Path | str): Path to the JSON config file, which must include
            "statement_configs", "selection", and "joins" sections.
        engine (sqlalchemy.Engine): A configured SQLAlchemy Engine.
        metadata (sqlalchemy.MetaData): A configured SQLAlchemy MetaData instance.

    Returns:
        sqlalchemy.Select: The constructed SQLAlchemy select statement.

    Raises:
        gdt.KnownException: If the config file is malformed or missing required sections.
    """
    try:
        with open(cfg_path, encoding="utf-8") as f:
            db_config = json.load(f)
        stmt_cfg = db_config.pop("statement_configs")
        selection = stmt_cfg["selection"]
        joins = stmt_cfg["joins"]
        alias = stmt_cfg["aliases"]

    except Exception as exc:
        raise gdt.KnownException(
            f"Config file {cfg_path} is malformed or missing : Should contain statement_configs, selection, and joins.",
        ) from exc

    statement = statement_builder(engine, metadata, selection, joins, alias)
    return statement


def statement_builder(
    engine: sqla.Engine,
    metadata: sqla.MetaData,
    selection: dict,
    joins: list[dict],
    alias: dict,
) -> sqla.Select:
    """Build an SQLAlchemy Select statement from a gswa-atratus config.

    Args:
        engine (sqlalchemy.Engine): A configured SQLAlchemy Engine.
        metadata (sqlalchemy.MetaData): A configured SQLAlchemy MetaData instance.
        selection (dict): Configured gswa-atratus dictionary specifying tables and columns.
        joins (list[dict]): Configured gswa-atratus dictionary detailing table joins.
        alias (dict): Configured gswa-atratus dictionary for alias mapping of tables.

    Returns:
        sqlalchemy.Select: "statement", an SQLAlchemy select statement.

    Raises:
        gdt.KnownException: For misconfigured software/network/selection config,
            missing tables or columns, or unavailable network/ODBC driver issues.
    """
    statement = None
    tables_to_alias = list(alias.keys())
    # retrieve tables
    tables_dict: dict[str, Any] = {}
    for t in list(selection.keys()):
        try:
            table_i = sqla.Table(t, metadata, autoload_with=engine)
            if t in tables_to_alias:
                tables_dict[alias[t]] = aliased(table_i, name=alias[t])
            else:
                tables_dict[t] = table_i
        except sqlae.InterfaceError as exc:
            raise gdt.KnownException(
                "There are several possible reasons for this error."
                " One possibility is that the ODBC driver specified"
                " in the config is not installed on your system."
            ) from exc
        except sqlae.NoSuchTableError as exc:
            raise gdt.KnownException(
                f"Table [{t}] specified in config, does not exist in engine."
            ) from exc
        except sqlae.OperationalError as exc:
            raise gdt.KnownException(
                f"Network connection to configured URL [{engine.url}] is not available."
                " Check network status or VPN."
            ) from exc

    # retrieve columns
    columns_list: list[sqla.Column] = []
    for table, column_list in selection.items():
        for col in column_list:
            try:
                if table in tables_to_alias:
                    t_aliased = tables_dict[alias[table]]
                else:
                    t_aliased = tables_dict[table]
                c = t_aliased.c[col]
                columns_list.append(c)
            except (KeyError, sqlae.NoSuchColumnError) as exc:
                raise gdt.KnownException(
                    f"Column [{col}] specified in config, does not exist in table."
                    f" [{table}] contains columns [{t_aliased.c.keys()}].",
                ) from exc
    statement = sqla.select(*columns_list)

    # add joins
    for j in joins:
        table_str = list(j.keys())[0]

        # extract_all strings
        mapping_list = j[table_str]
        left_table_str = mapping_list[0][0]
        right_table_str = mapping_list[1][0]
        left_col_str = mapping_list[0][1]
        right_col_str = mapping_list[1][1]

        t = (
            tables_dict[alias[table_str]]
            if table_str in tables_to_alias
            else tables_dict[table_str]
        )
        t_l = (
            tables_dict[alias[left_table_str]]
            if left_table_str in tables_to_alias
            else tables_dict[left_table_str]
        )
        t_r = (
            tables_dict[alias[right_table_str]]
            if right_table_str in tables_to_alias
            else tables_dict[right_table_str]
        )

        left_col = t_l.c[left_col_str]
        right_col = t_r.c[right_col_str]

        statement = statement.outerjoin(t, left_col == right_col)

    return statement
