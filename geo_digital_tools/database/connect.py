from pathlib import Path
import sqlite3
import pyodbc

import geo_digital_tools.utils.exceptions as gde

def connect_local_database(db_path: Path) -> sqlite3.Connection:

    con = sqlite3.connect(db_path)

    return con

def connect_remote_wamexdev() -> pyodbc.Connection:
    # TODO we need to pull this strings out however it's relatively low security risk
    # to connect it leverages windows login so will only work for authed users on network
    try:
        con = pyodbc.connect(r'Driver=SQL Server;Server=SQLD\DEV;Database=WAMEX;Trusted_Connection=yes;')
        return con
    except:
        gde.KnownException('Connection to WAMEX Failed')
        return None    

def check_valid_select(query_list : list[str]) -> list[str]:

    return None

def check_valid_create(query_list : list[str]) -> list[str]:
    
    temp_db = sqlite3.connect(":memory:")
    
    valid_queries = []

    for query in query_list:
        try:
            temp_db.execute(query)
            valid_queries.append(query)
        except Exception as e:
            gde.KnownException(f'Invalid SQLite Query {query} - {e}')

    temp_db.close()

    return valid_queries

def check_valid_sqlite(query_list : list[str]) -> list[str]:
    select_queries = [x for x in query_list if 'select' in x.lower()]
    create_queries = [x for x in query_list if 'create' in x.lower()]

    valid_select = check_valid_select(select_queries)
    valid_create = check_valid_create(create_queries)

    # some atttempt to preserve order incase it's important
    valid_queries = [q for q in query_list if q in valid_select or q in valid_create]

    return valid_queries