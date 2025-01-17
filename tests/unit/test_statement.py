import json
from pathlib import Path

import pandas as pd
import pytest
import sqlalchemy as sqla

import geo_digital_tools as gdt


@pytest.fixture
def mocked_db_valid() -> tuple[sqla.Engine, sqla.MetaData]:

    memory_engine = sqla.engine.engine_from_config(
        {"sqlalchemy.url": "sqlite+pysqlite:///:memory:"}
    )

    for t_number in [1, 2]:
        table = pd.DataFrame(
            {f"table_{t_number}_col_1": [1, 2, 3], f"table_{t_number}_col_2": [1, 2, 3]}
        )
        gdt.insert(memory_engine, f"table_{t_number}", table)

    return memory_engine, sqla.MetaData()


@pytest.fixture
def mocked_db_missing_table() -> tuple[sqla.Engine, sqla.MetaData]:

    memory_engine = sqla.engine.engine_from_config(
        {"sqlalchemy.url": "sqlite+pysqlite:///:memory:"}
    )

    for t_number in [1, 2]:
        table = pd.DataFrame(
            {f"table_{t_number}_col_1": [1, 2, 3], f"table_{t_number}_col_2": [1, 2, 3]}
        )
        gdt.insert(memory_engine, f"no_table_here_{t_number}", table)

    return memory_engine, sqla.MetaData()


@pytest.fixture
def mocked_db_missingcol() -> tuple[sqla.Engine, sqla.MetaData]:

    memory_engine = sqla.engine.engine_from_config(
        {"sqlalchemy.url": "sqlite+pysqlite:///:memory:"}
    )

    for t_number in [1, 2]:
        table = pd.DataFrame(
            {
                f"table_{t_number}_no_column_here_col_1": [1, 2, 3],
                f"table_{t_number}_col_2": [1, 2, 3],
            }
        )
        gdt.insert(memory_engine, f"table_{t_number}", table)

    return memory_engine, sqla.MetaData()


class TestStatement:
    @pytest.fixture
    def valid_cfg_memory(self):
        valid_config = {
            "statement_configs": {
                "selection": {
                    "table_1": ["table_1_col_1", "table_1_col_2"],
                    "table_2": ["table_2_col_1", "table_2_col_2"],
                },
                "joins": [
                    {
                        "table_2": [
                            ["table_2", "table_2_col_1"],
                            ["table_1", "table_1_col_1"],
                        ]
                    },
                    {
                        "table_2": [
                            ["table_2", "table_2_col_1"],
                            ["table_1", "table_1_col_1"],
                        ]
                    },
                ],
                "aliases": {"table_2": "table_2_label", "table_1": "table_1_label"},
            }
        }
        return valid_config

    @pytest.fixture
    def valid_cfg_disk(self, valid_cfg_memory, tmp_path) -> Path:
        cfg_path = tmp_path / "test_config.json"
        with open(cfg_path, "w") as f:
            json.dump(valid_cfg_memory, f)
        return cfg_path

    @pytest.fixture
    def invalid_cfg_disk(self, valid_cfg_memory, tmp_path) -> Path:
        cfg_path = tmp_path / "test_config.json"
        with open(cfg_path, "w") as f:
            json.dump({"foo": "bar"}, f)
        return cfg_path

    def test_valid_load_statement(self, mocked_db_valid, valid_cfg_disk):
        engine, meta_data = mocked_db_valid
        statement = gdt.load_statement(
            cfg_path=valid_cfg_disk,
            engine=engine,
            metadata=meta_data,
        )
        statement_str = str(statement)
        assert (
            statement_str
            == "SELECT table_1_label.table_1_col_1, table_1_label.table_1_col_2, table_2_label.table_2_col_1, table_2_label.table_2_col_2 \nFROM table_1 AS table_1_label JOIN table_2 AS table_2_label ON table_2_label.table_2_col_1 = table_1_label.table_1_col_1 JOIN table_2 AS table_2_label ON table_2_label.table_2_col_1 = table_1_label.table_1_col_1"
        )

    def test_bad_config(self, mocked_db_valid, invalid_cfg_disk):
        engine, meta_data = mocked_db_valid
        with pytest.raises(gdt.KnownException) as excinfo:
            selection, joins = gdt.load_statement(
                cfg_path=invalid_cfg_disk,
                engine=engine,
                metadata=meta_data,
            )
        assert "malformed or missing : Should" in str(excinfo.value)

    def test_statement_builder(self, mocked_db_valid, valid_cfg_memory):
        engine, metadata = mocked_db_valid

        selection = valid_cfg_memory["statement_configs"]["selection"]
        joins = valid_cfg_memory["statement_configs"]["joins"]
        aliases = valid_cfg_memory["statement_configs"]["aliases"]
        assert True
        statement = gdt.utils.statement_builder(
            metadata=metadata,
            engine=engine,
            selection=selection,
            joins=joins,
            alias=aliases,
        )
        statement_str = str(statement)
        assert (
            statement_str
            == "SELECT table_1_label.table_1_col_1, table_1_label.table_1_col_2, table_2_label.table_2_col_1, table_2_label.table_2_col_2 \nFROM table_1 AS table_1_label JOIN table_2 AS table_2_label ON table_2_label.table_2_col_1 = table_1_label.table_1_col_1 JOIN table_2 AS table_2_label ON table_2_label.table_2_col_1 = table_1_label.table_1_col_1"
        )

    def test_statement_builder_missingtable(
        self, mocked_db_missing_table, valid_cfg_memory
    ):

        engine, metadata = mocked_db_missing_table

        selection = valid_cfg_memory["statement_configs"]["selection"]
        joins = valid_cfg_memory["statement_configs"]["joins"]
        aliases = valid_cfg_memory["statement_configs"]["aliases"]

        with pytest.raises(gdt.KnownException) as excinfo:
            statement = gdt.utils.statement_builder(
                metadata=metadata,
                engine=engine,
                selection=selection,
                joins=joins,
                alias=aliases,
            )

        assert "specified in config, does not exist in engine." in str(excinfo.value)

    def test_statement_builder_missingcolumn(
        self, mocked_db_missingcol, valid_cfg_memory
    ):

        engine, metadata = mocked_db_missingcol

        selection = valid_cfg_memory["statement_configs"]["selection"]
        joins = valid_cfg_memory["statement_configs"]["joins"]
        aliases = valid_cfg_memory["statement_configs"]["aliases"]

        with pytest.raises(gdt.KnownException) as excinfo:
            statement = gdt.utils.statement_builder(
                metadata=metadata,
                engine=engine,
                selection=selection,
                joins=joins,
                alias=aliases,
            )

        assert "specified in config, does not exist in table" in str(excinfo.value)
