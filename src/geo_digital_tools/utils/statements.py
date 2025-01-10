import json
from pathlib import Path

import sqlalchemy as sqla
from sqlalchemy.orm import aliased
from sqlalchemy import exc as sqlae

import geo_digital_tools as gdt


def load_statement_config(cfg_path: Path | str) -> tuple[dict, dict]:
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

    return selection, joins, alias


def statement_builder(
    engine: sqla.Engine,
    metadata: sqla.MetaData,
    columns_dict: dict,
    join_list: list[dict],
    alias: dict,
):
    """
    Build an SQLAlchemy statement from a geo digital tools config.
    colummns : dict {table_name : [col1, col2]}
    """
    statement = None
    tables_to_alias = list(alias.keys())
    # retrieve tables
    tables_dict = {}
    for t in list(columns_dict.keys()):
        try:
            table_i = sqla.Table(t, metadata, autoload_with=engine)
            if t in tables_to_alias:
                tables_dict[alias[t]] = aliased(table_i, name=alias[t])
            if t not in tables_to_alias:
                tables_dict[t] = table_i

        except sqlae.NoSuchTableError:
            gdt.KnownException(
                f"Table [{t}] specified in config, does not exist in engine.",
                should_raise=True,
            )

    # retrieve columns
    columns_list = []
    for table, column_list in columns_dict.items():
        for col in column_list:
            try:
                if table in tables_to_alias:
                    t = tables_dict[alias[table]]
                if table not in tables_to_alias:
                    t = tables_dict[table]
                c = t.c[col]
                columns_list.append(c)
            except KeyError or sqlae.NoSuchColumnError:
                # TODO: Consider if an Exception group is appropriate here.
                gdt.KnownException(
                    f"Column [{col}] specified in config, does not exist in table [{table}] contains columns [{t.c.keys()}].",
                    should_raise=True,
                )
    statement = sqla.select(*columns_list)

    # add joins
    for j in join_list:

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
