import json
from pathlib import Path

import pytest
import sqlalchemy as sqla

from geo_digital_tools.database import METADATA  # This will be cleared for each test
from geo_digital_tools.database.connect import (
    SQLAConnection,
    load_db_config,
    remote_database,
    validate_db_config,
)
from geo_digital_tools.database.create_v2 import CreateInterface
from geo_digital_tools.database.read import ReadInterface
from geo_digital_tools.database.utils import (
    ColumnBuilder,
    check_valid_sqlite,
    dict_raise_on_duplicates,
    get_metadata,
    get_table,
    get_tables_names,
    interface_to_csv,
    parse_database_config,
    tables_from_config,
)
from geo_digital_tools.database.write import WriteInterface
from geo_digital_tools.utils import exceptions as gdte

valid_columns_json = {
    "big_integer_col": "BigInteger",
    "boolean_col": "Boolean",
    "datetime_col": "DateTime",
    "double_col": "Double",
    "float_col": "Float",
    "integer_col": "Integer",
    "large_binary_col": "LargeBinary",
    "numeric_col": "Numeric",
    "string_col": "String",
    "text_col": "Text",
    "uuid_col": "Uuid",
}

# Invalid column JSON with unsupported types
invalid_columns_json = {
    "valid_integer_col": "Integer",
    "unknown_type_col": "UnknownType",
}


@pytest.fixture()
def create_cfg(tmp_path):
    # Valid columns JSON structure with all supported SQLAlchemy types

    # Sample valid configuration for tables
    valid_config = {"table1": valid_columns_json}

    # Sample configuration path (adjust as needed or mock file)
    cfg_path = tmp_path / "test_config.json"
    with open(cfg_path, "w") as f:
        json.dump(valid_config, f)

    yield cfg_path, valid_config

    cfg_path.unlink()


@pytest.fixture()
def create_db():
    # Setup in-memory SQLite engine for testing
    engine = sqla.create_engine("sqlite:///:memory:")
    meta = sqla.MetaData()

    yield engine, meta
    # TODO check if we need to shutdown the engine.


@pytest.mark.skip(reason="Not implemented")
class TestConnect:
    def test_SQLAConnection(self):
        assert False

    def test_load_db_config(self):
        assert False

    def test_validate_db_config(self):
        assert False

    def test_remote_database(self):
        assert False


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
            ColumnBuilder(columns_json=invalid_columns_json)

    def test_tables_from_config(self, create_cfg, create_db):
        # Test table creation from valid configuration
        engine, meta = create_db
        tables_from_config(create_cfg[1], engine, meta)
        table_names = meta.tables.keys()
        assert "table1" in table_names

    def test_dict_raise_on_duplicates(self):
        # Test duplicate keys in configuration handling
        duplicate_config = [
            ("table1", {"col1": "String"}),
            ("table1", {"col2": "Integer"}),
        ]
        with pytest.raises(gdte.KnownException):
            dict_raise_on_duplicates(duplicate_config)

    def test_parse_database_config(self, create_cfg):
        # Test loading and parsing configuration file without duplicates
        config = parse_database_config(create_cfg[0])
        assert "table1" in config
        assert config["table1"] == valid_columns_json

    def test_parse_database_config_with_duplicates(self):
        # Test parsing with duplicate keys in the config
        # Note that Python will silently drop duplicated key:values in a dictionary
        # We check here if data has silently been lost

        test_value = "DateTime"
        invalid_config = (
            '{"table1": {"col1": "String"}, "table1": {"col1": "' + test_value + '"}}'
        )

        duplicate_config_path = Path("duplicate_test_config.json")
        with open(duplicate_config_path, "w") as f:
            f.write(invalid_config)

        with pytest.raises(gdte.KnownException):
            parse_database_config(duplicate_config_path)

        if duplicate_config_path.exists():
            duplicate_config_path.unlink()


@pytest.mark.skip(reason="Not implemented")
class TestRead:
    def test_x(self):
        assert 0


@pytest.mark.skip(reason="Not implemented")
class TestUpdate:
    def test_x(self):
        assert 0


@pytest.mark.skip(reason="Not implemented")
class TestWrite:
    def test_x(self):
        assert 0
