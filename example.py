import sqlalchemy as sqla

import geo_digital_tools as gdt
from geo_digital_tools.database import METADATA


class ExampleCreateInterface(gdt.CreateInterface):
    """Interface for creating the Example database"""

    def __init__(self, url=None, cfg_path=None):
        super().__init__(url, cfg_path)


class ExampleWriteInterface(gdt.WriteInterface):
    def __init__(self, engine: sqla.Engine):
        """Write interface designed for Example database"""
        super().__init__(engine=engine)

    def write(self, table, value_dict):
        """Defines how to write to Example"""
        with self.engine.begin() as conn:
            tbl = sqla.insert(table=table)
            result = conn.execute(tbl, value_dict)
            conn.commit()

        return result


class ExampleReadInterface(gdt.ReadInterface):
    def __init__(self, engine):
        """Read interface designed for Example database"""
        super().__init__(engine)

    def select_statement(self):
        """Select 'col1' and 'col2' columns from 'table1' table in engine"""
        try:
            files = sqla.Table("table1", METADATA, autoload_with=self.engine)
        except sqla.exc.NoSuchTableError as exc:
            gdt.KnownException(
                f"Read Interface : Table '{exc}' is not available in {type(self).__name__}.",
                should_raise=True,
            )

        try:
            stmt = sqla.select(files.c.col1, files.c.col2)
        except AttributeError as exc:
            gdt.KnownException(
                f"Read Interface : Column '{exc}' does not exist in Table"
            )

        return stmt


if __name__ == "__main__":
    """Demo program of working with a new local database"""
    print("\nTime to create!")
    # Create a database (alternatively load one with connect)
    example_create = ExampleCreateInterface(cfg_path="configs/_example_cfg.json")
    # OR example_create.define_db() if using "code" style definition
    example_create.create_metadata()
    example_engine = example_create.engine

    print("\nTime to write!")
    example_write = ExampleWriteInterface(engine=example_engine)

    table_names = gdt.database.get_tables_names(example_engine)

    dest_table = "table1"
    table = METADATA.tables[dest_table]
    if dest_table not in table_names:
        gdt.KnownException(
            f"Intended destination table '{dest_table}' does not exist "
            f"in '{example_write}'. Available tables are: {table_names}"
        )

    value_dict = [
        {"col1": "hello", "col2": 123},
        {"col1": "world", "col2": 42},
    ]

    result = example_write.write(table=table, value_dict=value_dict)
    print(result.last_inserted_params())

    print("\nTime to read!")
    example_read = ExampleReadInterface(engine=example_engine)
    example_read.validate_interface()
    example_df = example_read.df_from_interface()
    # example_read.query_interface()
    # example_df = example_read.query_to_df()
    print(example_df)

    print("\nI'm Done!")
