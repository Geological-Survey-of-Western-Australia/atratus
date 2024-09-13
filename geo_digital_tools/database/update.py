import sqlite3
import sqlalchemy as db

from geo_digital_tools.database.read import get_table_schema_as_dict, get_tables_names
import geo_digital_tools.utils.exceptions as gdte

def df_to_entry(pdf_match):
    """
    The input dataframe should have columns that correspond to the columns in the sql table.
    """
    entry_list = []
    for row_dict in pdf_match.to_dict(orient="records"):
        entry_list.append(row_dict)

    return entry_list


def remove_duplicates(entry_list, stored_list: list[str], duplicate_field: str):
    # duplicates in submission
    unique_sumbitted_hashes = list(set([e[duplicate_field] for e in entry_list]))
    # duplicates in storage
    duplicates_of_stored_hashes = [
        h for h in unique_sumbitted_hashes if h in stored_list
    ]

    # if it's not 1 to 1 it means the set removed duplicates
    if len(unique_sumbitted_hashes) != len(entry_list):
        print("Duplicates found in Submission")

    if len(duplicates_of_stored_hashes) != 0:
        print("Duplicates found in Database")

    entry_list_unique_new = []
    # for each new hash
    for hash in unique_sumbitted_hashes:
        if hash not in duplicates_of_stored_hashes:
            first_match = [e for e in entry_list if e[duplicate_field] == hash][0]
            entry_list_unique_new.append(first_match)
    return entry_list_unique_new


def write_to_table(
    connection: sqlite3.Connection,
    entry_list: list[dict],
    table_name: str,
    duplicate_field: str = "",
):

    # check table in connection
    table_list = get_tables_names(connection)
    table_schema = get_table_schema_as_dict(connection, table_name)

    if table_name not in table_list:
        gdte.KnownException("Table not found in connection skipping.", level="critcal")
    if len(entry_list) == 0:
        gdte.KnownException("Entry list Empty Skipping", level="critical")
    else:
        if entry_list[0].keys() == table_schema.keys():
            gdte.KnownException(
                f"Table and Entry Schema error {entry_list[0].keys()} != {table_schema.keys()}",
                level="critical",
            )

        if duplicate_field != "" and duplicate_field in list(table_schema.keys()):
            print("Checking for Duplicates")
            result = connection.execute(f"select {duplicate_field} from {table_name}")
            exisiting_filehash = [v[0] for v in result.fetchall()]
            no_dupes = remove_duplicates(
                entry_list, exisiting_filehash, duplicate_field
            )
            if len(no_dupes) != 0:
                entry_list = no_dupes

        # write the non duplicated entries to the db
        table_col_str = f"{table_name}{str(tuple(entry_list[0].keys()))}"
        question_str = ",".join(["?"] * len(list(entry_list[0].keys())))
        sql_tuple_list = [tuple([str(x) for x in d.values()]) for d in entry_list]
        connection.executemany(
            f"insert into {table_col_str} values ({question_str})",
            sql_tuple_list,
        )
        connection.commit()


def update_table(database_engine, table_name : str, update_statement : db.sql.dml.Update):
    '''
    sqlAlchemy statement objects are fascinating.

    # Example db_engine
    engine = db.create_engine(r"sqlite:///E:\wamex_rdb.sqlite")

    # Example Statment
    update_statement = (db.update(files)
                    .where(files.c.anumber =='None')
                    .values(anumber=get_anumber(files.c.file_path)))
    '''

    connection = database_engine.connect()
    metadata = db.MetaData()

    # connect to key tables
    files = db.Table(table_name, metadata, autoload_with=database_engine)
    connection.execute(update_statement)
    connection.commit()
