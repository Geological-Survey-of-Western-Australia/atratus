import sqlalchemy as sqla
from sqlalchemy import exc as sqlae
from pathlib import Path
import json
import geo_digital_tools as gdt


def load_statement_config(cfg_path: Path | str) -> dict:
    try:
        with open(cfg_path) as f:
            db_config = json.load(f)
        stmt_cfg = db_config.pop("statement_configs")
        selection = stmt_cfg["selection"]
        joins = stmt_cfg["joins"]

    except Exception as e:
        gdt.KnownException(
            f"Config file {cfg_path} is malformed : Should contain statement_configs, selection, and joins."
        )

    return selection, joins


def statement_builder(metadata, engine, columns_dict, join_list):
    """
    colummns : dict {table_name : [col1, col2]}
    """
    statement = None

    # retrieve tables
    tables_dict = {}
    for t in list(columns_dict.keys()):
        try:
            tables_dict[t] = sqla.Table(t, metadata, autoload_with=engine)
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
                c = tables_dict[table].c[col]
                columns_list.append(c)
            except sqlae.NoSuchColumnError:
                gdt.KnownException(
                    f"Column [{col}] specified in config, does not exist in table [{table}].",
                    should_raise=True,
                )
    statement = sqla.select(*columns_list)

    # add joins
    for j in join_list:

        target_str = list(j.keys())[0]
        mapping_list = j[target_str]

        target = tables_dict[target_str]
        left_col = tables_dict[mapping_list[0][0]].c[mapping_list[0][1]]
        right_col = tables_dict[mapping_list[1][0]].c[mapping_list[1][1]]

        statement = statement.join(target, left_col == right_col)

    return statement
