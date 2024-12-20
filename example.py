import sqlalchemy as sqla

import geo_digital_tools as gdt
from geo_digital_tools.database import METADATA


class AtratusCreateInterface(gdt.CreateInterface):
    """Interface for creating the Atratus database"""

    def __init__(self, url=None, cfg_path=None):
        super().__init__(url, cfg_path)


class AtratusWriteInterface(gdt.WriteInterface):
    def __init__(self, engine: sqla.Engine):
        """Write interface designed for Atratus"""
        super().__init__(engine=engine)

    def write(self, table, value_dict):
        """Defines how to write to Atratus"""
        with self.engine.begin() as conn:
            # result = conn.execute(stmt)
            tbl = sqla.insert(table=table)
            # compiled = stmt.compile()

            result = conn.execute(tbl, value_dict)
            conn.commit()

        return result


class AtratusReadInterface(gdt.ReadInterface):
    def __init__(self, engine):
        """Read interface designed for Atratus"""
        super().__init__(engine)

    def select_statement(self):
        """Select 'ANumber' and 'file_name' columns from 'files' table in engine"""
        try:
            files = sqla.Table("files", METADATA, autoload_with=self.engine)
        except sqla.exc.NoSuchTableError as exc:
            gdt.KnownException(
                f"Read Interface : Table '{exc}' is not available in {type(self).__name__}.",
                should_raise=True,
            )

        try:
            stmt = sqla.select(files.c.ANumber, files.c.file_name)
        except AttributeError as exc:
            gdt.KnownException(
                f"Read Interface : Column '{exc}' does not exist in Table"
            )

        return stmt


if __name__ == "__main__":
    """Demo program of working with a new local database"""
    print("\nTime to create!")
    # Create a database (alternatively load one with connect)
    atratus_create = AtratusCreateInterface(cfg_path="configs/atratus.json")
    # OR atratus_create.define_db() if using "code" style definition
    atratus_create.create_metadata()
    atratus_engine = atratus_create.engine

    print("\nTime to write!")
    atratus_write = AtratusWriteInterface(engine=atratus_engine)

    table_names = gdt.database.get_tables_names(atratus_engine)

    dest_table = "files"
    table = METADATA.tables[dest_table]
    if dest_table not in table_names:
        gdt.KnownException(
            f"Intended destination table '{dest_table}' does not exist "
            f"in '{atratus_write}'. Available tables are: {table_names}"
        )

    value_dict = [
        {"ANumber": "999999", "file_name": "test_file"},
        {"ANumber": "9999999", "file_name": "another_file"},
    ]
    # value_dict = {"ANumber": [999999, 9999999],"file_name": ["test_file", "another_file"]} # Pandas Style

    result = atratus_write.write(table=table, value_dict=value_dict)
    print(result.last_inserted_params())

    print("\nTime to read!")
    atratus_read = AtratusReadInterface(engine=atratus_engine)
    atratus_read.validate_interface()
    atratus_df = atratus_read.df_from_interface()
    # atratus_read.query_interface()
    # atratus_df = atratus_read.query_to_df()
    print(atratus_df)

    print("\nI'm Done!")
