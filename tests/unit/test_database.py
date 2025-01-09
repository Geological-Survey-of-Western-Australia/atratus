import json
from pathlib import Path
import pandas as pd
import sqlalchemy as sqla
import pytest
import geo_digital_tools as gdt


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
        """Valid columns JSON structure with all supported SQLAlchemy types"""
        valid_config = {"sqlalchemy": {"sqlalchemy.url": "bar"}}
        cfg_path = tmp_path / "test_config.json"
        with open(cfg_path, "w") as f:
            json.dump(valid_config, f)
        return cfg_path, valid_config

    def test_returns_engine_metadata(self, valid_cfg):
        engine, metadata = gdt.connect(cfg_path=valid_cfg[0])
        assert isinstance(engine, sqla.Engine) and isinstance(metadata, sqla.MetaData)

    def test_connect_config_missing(self):
        with pytest.raises(FileNotFoundError):
            result = gdt.connect(cfg_path=Path("C:silly_path.json"))

    def test_connect_missing_key(self, missing_key_cfg):
        # NOTE given that this is something missing from a 'gdt' file perhaps it should also
        # raise a gdt.KnownException to warn the user of a bad config?
        # might be worth adding caplog to ensure certain messages are raised
        with pytest.raises(KeyError):
            result = gdt.connect(cfg_path=missing_key_cfg[0])

    def test_connect_bad_url(self, bad_url_cfg):
        # NOTE might be worth adding caplog to ensure certain messages are raised
        with pytest.raises(gdt.KnownException):
            result = gdt.connect(cfg_path=bad_url_cfg[0])


class TestCreate:
    def test_valid_column_builder(self):
        # Test ColumnBuilder with valid columns JSON
        builder = ColumnBuilder(columns_json=valid_columns_json)
        columns = builder.columns
        assert len(columns) == len(valid_columns_json)
        for column in columns:
            col_name = column.name
            col_type = column.type.__class__.__name__
            expected_type = valid_columns_json[col_name]
            assert col_type is expected_type

    def test_invalid_column_type(self):
        # Test ColumnBuilder with unsupported column types
        with pytest.raises(gdte.KnownException):
            ColumnBuilder(
                columns_json={
                    "valid_integer_col": "Integer",
                    "unknown_type_col": "UnknownType",
                }
            )

    def test_dict_raise_on_duplicates(self):
        # Test duplicate keys in configuration handling
        duplicate_config = [
            ("table1", {"col1": "String"}),
            ("table1", {"col2": "Integer"}),
        ]
        with pytest.raises(gdte.KnownException):
            dict_raise_on_duplicates(duplicate_config)

    def test_parse_database_config_dict(self, valid_cfg):
        """Test loading and parsing configuration file without duplicates"""
        config = parse_database_config(valid_cfg[0])
        assert "table1" in config["tables"]

    def test_tables_from_config_file(self, valid_cfg):
        """Test table creation from valid configuration dict"""
        tables_from_config(valid_cfg[1])
        table_names = METADATA.tables.keys()
        assert "table1" in table_names


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
