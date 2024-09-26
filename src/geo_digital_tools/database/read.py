import sqlite3
import warnings
import pandas as pd

# FIXME Refactor all functions to use sqlalchemy

def get_tables_names(connection: sqlite3.Connection) -> list[str]:
    cursor = connection.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

    return [s[0] for s in cursor.fetchall()]

def get_table_schema_as_dict(connection : sqlite3.Connection, target_table: str):
    tables = get_tables_names(connection)
    if target_table not in tables:
        warnings.warn(f"Table {target_table} not found in connection. Skipping.")
        return {}
    else:
        cursor = connection.cursor()
        cursor.execute(f"pragma table_info('{target_table}')")
        schema = cursor.fetchall()
        return {x[1]: x[2] for x in schema}

def result_to_df(result,col_name_list=[]):
    num_fields = len(result[0])
    if col_name_list==[] or len(col_name_list)!=num_fields:
        col_name_list = ['COL: '+str(i) for i in range(num_fields)]

    df_dict = {}
    for i in range(num_fields):
        df_dict[col_name_list[i]]= [x[i] for x in result]

    return pd.DataFrame(df_dict)

def entry_to_df(entry_list):
    df_dict = {k: [] for k in entry_list[0].keys()}
    for entry in entry_list:
        for k, v in entry.items():
            df_dict[k].append(v)

    result = pd.DataFrame(df_dict)
    return result