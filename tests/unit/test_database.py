import json
from pathlib import Path

import pandas as pd
import pytest
import sqlalchemy as sqla

import geo_digital_tools as gdt


@pytest.fixture
def mocked_populated_db(
    mocked_connect, dummy_data
) -> tuple[sqla.Engine, sqla.MetaData]:
    """Create a mocked database with dummy data."""
    engine = mocked_connect[0]
    metadata = mocked_connect[1]
    data_df = dummy_data[1]
    gdt.create_from_dataframe(engine, metadata, data_df, "test_select")
    return (engine, metadata, data_df)


@pytest.fixture
def dummy_data(tmp_path) -> tuple[str | Path, pd.DataFrame]:
    """Create dummy data as a DataFrame and save it as a CSV file."""
    test_data = {}
    test_data["col_1"] = [1, 1, 1, 1, 1]
    test_data["col_2"] = ["two", "two", "two", "two", "two"]
    test_data["col_3"] = [3.0, 3.0, 3.0, 3.0, 3.0]

    data_path = tmp_path / "test_data.csv"
    data_load = pd.DataFrame(test_data)
    data_load.to_csv(data_path)

    return data_path, data_load


@pytest.fixture
def mocked_connect() -> tuple[sqla.Engine, sqla.MetaData]:
    """Create a mock in-memory SQLite database."""
    memory_engine = sqla.engine.engine_from_config(
        {"sqlalchemy.url": "sqlite+pysqlite:///:memory:"}
    )
    return memory_engine, sqla.MetaData()


# Test class for database connection functionalities
class TestConnect:
    @pytest.fixture
    def valid_cfg(self, tmp_path) -> tuple[Path, dict]:
        """Valid columns JSON structure with all supported SQLAlchemy types"""
        valid_config = {"sqlalchemy": {"sqlalchemy.url": "sqlite+pysqlite:///:memory:"}}
        cfg_path = tmp_path / "test_config.json"
        with open(cfg_path, "w") as f:
            json.dump(valid_config, f)
        return cfg_path, valid_config

    @pytest.fixture
    def missing_key_cfg(self, tmp_path) -> tuple[Path, dict]:
        """Valid columns JSON structure with all supported SQLAlchemy types"""
        valid_config = {"foo": {"sqlalchemy.url": "sqlite+pysqlite:///:memory:"}}
        cfg_path = tmp_path / "test_config.json"
        with open(cfg_path, "w") as f:
            json.dump(valid_config, f)
        return cfg_path, valid_config

    @pytest.fixture
    def bad_url_cfg(self, tmp_path) -> tuple[Path, dict]:
        """Invalid JSON config file with a malformed URL."""
        valid_config = {"sqlalchemy": {"sqlalchemy.url": "bar"}}
        cfg_path = tmp_path / "test_config.json"
        with open(cfg_path, "w") as f:
            json.dump(valid_config, f)
        return cfg_path, valid_config

    def test_returns_engine_metadata(self, valid_cfg):
        """Test if a valid config file returns a SQLAlchemy engine and metadata."""
        engine, metadata = gdt.connect(cfg_path=valid_cfg[0])
        assert isinstance(engine, sqla.Engine) and isinstance(metadata, sqla.MetaData)

    def test_connect_config_missing(self):
        """Test if a missing config file raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            result = gdt.connect(cfg_path=Path("C:silly_path.json"))

    def test_connect_missing_key(self, missing_key_cfg):
        """Test if a config file with a missing key raises KeyError."""
        # NOTE given that this is something missing from a 'gdt' file perhaps it should also
        # raise a gdt.KnownException to warn the user of a bad config?
        # might be worth adding caplog to ensure certain messages are raised
        with pytest.raises(KeyError):
            result = gdt.connect(cfg_path=missing_key_cfg[0])

    def test_connect_bad_url(self, bad_url_cfg):
        """Test that gdt.connect raises the appropriate exception for a malformed URL."""
        # NOTE might be worth adding caplog to ensure certain messages are raised
        with pytest.raises(gdt.KnownException):
            result = gdt.connect(cfg_path=bad_url_cfg[0])


class TestCreate:
    def test_create_from_dataframe(self, mocked_connect, dummy_data):
        """Test if a table can be created from a DataFrame."""
        engine = mocked_connect[0]
        metadata = mocked_connect[1]

        data = dummy_data[1]

        gdt.create_from_dataframe(engine, metadata, dataframe=data)

        # assert table with expected columns created in engine
        metadata.reflect(engine)
        tables = metadata.tables.keys()
        assert "unnamed_table" in tables

    def test_create_name_table(self, mocked_connect, dummy_data):
        """Test if a named table can be created from a DataFrame."""
        engine = mocked_connect[0]
        metadata = mocked_connect[1]

        data = dummy_data[1]

        gdt.create_from_dataframe(
            engine,
            metadata,
            table_name="my_table_from_df",
            dataframe=data,
        )

        # assert table with expected columns created in engine
        metadata.reflect(engine)
        tables = metadata.tables.keys()
        assert all([True if tn in tables else False for tn in ["my_table_from_df"]])


class TestSelect:
    def test_select(self, mocked_populated_db):
        """Test if data can be selected from a table and matches the source DataFrame."""
        engine = mocked_populated_db[0]
        metadata = mocked_populated_db[1]
        source_df = mocked_populated_db[2]

        # generate a select statement for the dummy data
        metadata.reflect(engine)
        test_select = metadata.tables["test_select"]
        statement = sqla.select(test_select)

        result_df = gdt.select(engine=engine, statement=statement)

        assert result_df.equals(source_df)


class TestInsert:
    def test_insert(self, mocked_populated_db):
        """Test if data can be inserted into a new table and matches the original data."""
        engine = mocked_populated_db[0]
        metadata = mocked_populated_db[1]
        source_df = mocked_populated_db[2]

        # generate a select statement for the dummy data
        metadata.reflect(engine)
        test_select = metadata.tables["test_select"]
        statement = sqla.select(test_select)
        result_of_select_df = gdt.select(engine=engine, statement=statement)

        # insert a copy of it into a new table
        gdt.insert(engine, "my_test_table", source_df)

        # retrieve it
        metadata.reflect(engine)
        test_insert = metadata.tables["my_test_table"]
        select_inserted = sqla.select(test_insert)
        result_of_insert_df = gdt.select(engine, select_inserted)

        assert result_of_insert_df.equals(result_of_select_df)


# # @pytest.fixture(autouse=True)
# # def clear_metadata():
# #     """Clear metadata between tests."""
# #     METADATA.clear()


# # class TestRead:
# #     def test_read_interface(self, create_db):
# #         """Create a Mock ReadInterface and ensure the contained value can be read"""

# #         class MockReadInterface(ReadInterface):
# #             def __init__(self, engine):
# #                 super().__init__(engine)

# #             def select_statement(self):
# #                 tbl = sqla.Table("table1", METADATA)
# #                 stmt = sqla.select(tbl.c.col1)
# #                 return stmt

# #         t_ri = MockReadInterface(create_db)
# #         t_ri.validate_interface()
# #         df = t_ri.df_from_interface()
# #         assert "check_value" in df["col1"][0]


# # @pytest.mark.skip(reason="Not implemented")
# # class TestUpdate:
# #     def test_update(self):
# #         assert False


# # class TestWrite:
# #     """Group of functionality from write.py"""

# #     def test_WriteInterface(create_db):
# #         t_wi = WriteInterface(create_db)
