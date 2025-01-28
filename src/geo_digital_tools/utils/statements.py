import json
from pathlib import Path

import sqlalchemy as sqla
from sqlalchemy.orm import aliased
from sqlalchemy import exc as sqlae

import geo_digital_tools as gdt


def load_statement(
    cfg_path: Path | str, engine: sqla.Engine, metadata: sqla.MetaData
) -> sqla.Select:
    """Load a geo digital tools config defining your SQL statement."""
    try:
        with open(cfg_path) as f:
            db_config = json.load(f)
        stmt_cfg = db_config.pop("statement_configs")
        selection = stmt_cfg["selection"]
        joins = stmt_cfg["joins"]
        alias = stmt_cfg["aliases"]

    except Exception as exc:
        gdt.KnownException(
            f"Config file {cfg_path} is malformed or missing : Should contain statement_configs, selection, and joins.",
            should_raise=True,
        )

    statement = statement_builder(engine, metadata, selection, joins, alias)
    return statement


def statement_builder(
    engine: sqla.Engine,
    metadata: sqla.MetaData,
    selection: dict,
    joins: list[dict],
    alias: dict,
) -> sqla.Select:
    """
    Build an SQLAlchemy statement from a geo digital tools config.
    """
    statement = None
    tables_to_alias = list(alias.keys())
    # retrieve tables
    tables_dict = {}
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
    columns_list = []
    for table, column_list in selection.items():
        for col in column_list:
            try:
                if table in tables_to_alias:
                    t = tables_dict[alias[table]]
                else:
                    t = tables_dict[table]
                c = t.c[col]
                columns_list.append(c)
            except (KeyError, sqlae.NoSuchColumnError) as exc:
                raise gdt.KnownException(
                    f"Column [{col}] specified in config, does not exist in table."
                    f" [{table}] contains columns [{t.c.keys()}].",
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

        statement = statement.join(t, left_col == right_col)

    return statement
