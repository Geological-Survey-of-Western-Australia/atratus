import unittest
import json
import sqlalchemy as sqla
from pathlib import Path
from geo_digital_tools.utils import exceptions as gdte
from geo_digital_tools.database.create import (
    ColumnBuilder,
    tables_from_config,
    dict_raise_on_duplicates,
    parse_database_config,
)  # Replace 'create' with your actual module name


class TestDatabaseFunctions(unittest.TestCase):
    def setUp(self):
        # Setup in-memory SQLite engine for testing
        self.engine = sqla.create_engine("sqlite:///:memory:")
        self.meta = sqla.MetaData()

        # Valid columns JSON structure with all supported SQLAlchemy types
        self.valid_columns_json = {
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
        self.invalid_columns_json = {
            "valid_integer_col": "Integer",
            "unknown_type_col": "UnknownType",
        }

        # Sample valid configuration for tables
        self.valid_config = {"table1": self.valid_columns_json}

        # Sample configuration path (adjust as needed or mock file)
        self.config_path = Path("test_config.json")
        with open(self.config_path, "w") as f:
            json.dump(self.valid_config, f)

    def tearDown(self):
        # Clean up created files after tests
        if self.config_path.exists():
            self.config_path.unlink()

    def test_valid_column_builder(self):
        # Test ColumnBuilder with valid columns JSON
        builder = ColumnBuilder(columns_json=self.valid_columns_json)
        columns = builder.columns
        self.assertEqual(len(columns), len(self.valid_columns_json))
        for column in columns:
            col_name = column.name
            col_type = column.type.__class__.__name__
            expected_type = self.valid_columns_json[col_name]
            self.assertEqual(col_type, expected_type)

    def test_invalid_column_type(self):
        # Test ColumnBuilder with unsupported column types
        with self.assertRaises(gdte.KnownException):
            ColumnBuilder(columns_json=self.invalid_columns_json)

    def test_tables_from_config(self):
        # Test table creation from valid configuration
        tables_from_config(self.valid_config, self.engine, self.meta)
        table_names = self.meta.tables.keys()
        self.assertIn("table1", table_names)

    def test_dict_raise_on_duplicates(self):
        # Test duplicate keys in configuration handling
        duplicate_config = [
            ("table1", {"col1": "String"}),
            ("table1", {"col2": "Integer"}),
        ]
        with self.assertRaises(gdte.KnownException):
            dict_raise_on_duplicates(duplicate_config)

    def test_parse_database_config(self):
        # Test loading and parsing configuration file without duplicates
        config = parse_database_config(self.config_path)
        self.assertIn("table1", config)
        self.assertEqual(config["table1"], self.valid_columns_json)

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

        with self.assertRaises(gdte.KnownException):
            parse_database_config(duplicate_config_path)

        if duplicate_config_path.exists():
            duplicate_config_path.unlink()


if __name__ == "__main__":
    unittest.main()
