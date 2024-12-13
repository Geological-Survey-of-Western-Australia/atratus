import sqlalchemy as sqla
import geo_digital_tools as gdt
import pandas as pd


class AtratusLocalInterface(gdt.CreateInterface):
    """Interface for creating the Atratus database"""

    def __init__(self, url=None, cfg_path=None):
        super().__init__(url, cfg_path)


class AtratusWriteInterface(gdt.WriteInterface):
    """Interface for writing to the Atratus database"""

    def __init__(self, engine: sqla.Engine):
        super().__init__(engine=engine)

    def write(self, stmt):
        """Method to define how to write to Atratus"""
        with self.engine.begin() as conn:
            result = conn.execute(stmt)

        return result


if __name__ == "__main__":
    """Demo program of writing to a database"""
    # Create a database (alternatively load one with connect)
    # Create database engine and metadata
    atratus_local = AtratusLocalInterface(cfg_path="configs/atratus.json")
    # OR atratus_local.define_db() if using "code" style definition
    atratus_local.create_metadata()
    atratus_engine = atratus_local.engine

    # Alternative for existing DB
    # # Connect to a database engine and load metadata
    # al = AtratusConnect("Atratus_remote_config.json")

    table_names = gdt.database.get_tables_names(atratus_engine)
    atratus_write = AtratusWriteInterface(atratus_engine)

    data = pd.DataFrame(
        {
            "woah": [20],
            "oh_my": "derp",
        }
    )

    dest_table = "files"
    assert dest_table in table_names

    df = pd.DataFrame(data)
    atratus_write.write(df, dest_table)
