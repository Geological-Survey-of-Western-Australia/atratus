import pandas as pd
import sqlalchemy as sqla
import geo_digital_tools.utils.exceptions as gde


def get_tables_names(engine: sqla.Engine) -> list[str]:
    """
    This just loads the existing table names and runs faster than meta-data reflect.
    It does not load schemas.
    """
    list_of_tables = []

    try:
        inspector = sqla.engine.reflection.Inspector.from_engine(engine)
        list_of_tables = inspector.get_table_names()
    except Exception as e:
        gde.KnownException(
            f"GDT - Found ecountered exception {e} when getting table names."
        )

    if len(list_of_tables) == 0:
        gde.KnownException("GDT - Found no tables in engine.")

    return list_of_tables


def get_table(
    engine: sqla.Engine, target_table: str, return_schema_as_dict=False
) -> sqla.Table | None | dict:
    """
    Gets an sqla table from the engine.
    If table name in engines tables returns table.
    Else logs and returns None
    NOTE should this be pulled out into two functions?
    """

    tables = get_tables_names(engine)

    if target_table not in tables:
        gde.KnownException(f"Table {target_table} not found in engine. Skipping.")
        return None
    else:
        meta_data = sqla.MetaData()
        TargetTable = sqla.Table(target_table, meta_data, autoload_with=engine)

        if return_schema_as_dict:
            schema_as_dict = {k: str(v.type) for k, v in TargetTable.columns.items()}
            return schema_as_dict

        elif not return_schema_as_dict:
            return TargetTable


def result_to_df(result: list[tuple], col_name_list: list[str] = []) -> pd.DataFrame:
    """
    utility function to quickly create pandas dataframe from result
    """

    num_fields = len(result[0])

    if col_name_list == [] or len(col_name_list) != num_fields:
        col_name_list = ["COL: " + str(i) for i in range(num_fields)]

    df_dict = {}

    for i in range(num_fields):
        df_dict[col_name_list[i]] = [x[i] for x in result]

    return pd.DataFrame(df_dict)


def entry_to_df(entry_list: list[dict]) -> pd.DataFrame:
    """
    Some results are surved as a list of dictionaries.

    This function extracts the keys from the entry list and quickly builds a df.
    """
    df_dict = {k: [] for k in entry_list[0].keys()}

    for entry in entry_list:
        for k, v in entry.items():
            df_dict[k].append(v)

    result = pd.DataFrame(df_dict)

    return result
