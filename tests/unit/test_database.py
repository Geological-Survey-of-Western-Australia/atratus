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


@pytest.fixture(autouse=True)
def clear_metadata():
    """Clear metadata between tests."""
    METADATA.clear()


@pytest.fixture()
def valid_cfg(tmp_path):
    """Valid columns JSON structure with all supported SQLAlchemy types"""
    valid_config = {
        "sqlalchemy": {"sqlalchemy.url": "sqlite+pysqlite:///:memory:"},
        "tables": {"table1": {"col1": "String", "col2": "Integer"}},
    }
    cfg_path = tmp_path / "test_config.json"
    with open(cfg_path, "w") as f:
        json.dump(valid_config, f)

    yield cfg_path, valid_config


@pytest.fixture()
def invalid_cfg(tmp_path):
    """Config from a text file that contains duplicated tables.
    These may be lost when converted to a python dict.
    """
    invalid_config_text = (
        '{"sqlalchemy": {"sqlalchemy.url": "sqlite+pysqlite:///:memory:"},'
        '"tables": {"table1": {"col1": "String"}, "table1": {"col1": "DateTime"}}'
    )
    cfg_path = tmp_path / "test_config.json"
    cfg_path.write_text(invalid_config_text)

    yield (cfg_path,)


@pytest.fixture()
def create_engine(valid_cfg):
    """Setup in-memory SQLite engine"""
    cfg = valid_cfg[1].pop("sqlalchemy")
    engine = sqla.engine_from_config(cfg)
    yield engine


@pytest.fixture()
def create_db(create_engine: sqla.Engine, valid_cfg: dict):
    """A DB with table 'table1', column 'col1', as degined in valid_cfg,
    with inserted 'check_value'
    """
    engine = create_engine
    tables_from_config(valid_cfg[1])
    METADATA.create_all(engine)
    stmt = sqla.insert(sqla.Table("table1", METADATA)).values(col1="check_value")
    stmt.compile()
    with engine.connect() as conn:
        conn.execute(stmt)
        conn.commit()

    yield engine


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

    def test_parse_database_config_with_duplicates(self, invalid_cfg):
        """Test parsing with duplicate keys in the config

        Note that Python will silently drop duplicated key:values in a dictionary
        We check here if data will be silently been lost
        """
        with pytest.raises(gdte.KnownException):
            parse_database_config(invalid_cfg[0])

    def test_createinterface_from_config(self, valid_cfg):
        t_if = CreateInterface(cfg_path=valid_cfg[0])
        t_if.create_metadata()
        assert "table1" in sqla.inspect(t_if.engine).get_table_names()


class TestRead:
    def test_read_interface(self, create_db):
        """Create a Mock ReadInterface and ensure the contained value can be read"""

        class MockReadInterface(ReadInterface):
            def __init__(self, engine):
                super().__init__(engine)

            def select_statement(self):
                tbl = sqla.Table("table1", METADATA)
                stmt = sqla.select(tbl.c.col1)
                return stmt

        t_ri = MockReadInterface(create_db)
        t_ri.validate_interface()
        df = t_ri.df_from_interface()
        assert "check_value" in df["col1"][0]


@pytest.mark.skip(reason="Not implemented")
class TestUpdate:
    def test_update(self):
        assert False


class TestWrite:
    """Group of functionality from write.py"""

    def test_WriteInterface(create_db):
        t_wi = WriteInterface(create_db)
