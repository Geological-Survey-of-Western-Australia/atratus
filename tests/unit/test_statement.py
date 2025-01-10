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
                    }
                ],
            },
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

    def test_load_valid_statement_config(self, valid_cfg_disk):
        selection, joins = gdt.load_statement_config(cfg_path=valid_cfg_disk)
        for k, v in selection.items():
            assert isinstance(k, str)
            assert isinstance(v, list)
            for i in v:
                assert isinstance(i, str)

        for j in joins:
            for k, v in j.items():
                assert isinstance(k, str)
                assert isinstance(v, list)
                for i in v:
                    assert isinstance(i, list)
                    for ii in i:
                        assert isinstance(ii, str)

    def test_bad_config(self, invalid_cfg_disk):
        with pytest.raises(gdt.KnownException) as excinfo:
            selection, joins = gdt.load_statement_config(cfg_path=invalid_cfg_disk)
        assert "malformed or missing : Should" in str(excinfo.value)

    def test_statement_builder(self, mocked_db_valid, valid_cfg_memory):

        engine, metadata = mocked_db_valid

        tables_dict = valid_cfg_memory["statement_configs"]["selection"]
        joins = valid_cfg_memory["statement_configs"]["joins"]

        statement = gdt.statement_builder(
            metadata=metadata, engine=engine, columns_dict=tables_dict, join_list=joins
        )

        assert (
            str(statement).replace("\n", "")
            == "SELECT table_1.table_1_col_1, table_1.table_1_col_2, table_2.table_2_col_1, table_2.table_2_col_2 FROM table_1 JOIN table_2 ON table_2.table_2_col_1 = table_1.table_1_col_1"
        )

    def test_statement_builder_missingtable(
        self, mocked_db_missing_table, valid_cfg_memory
    ):

        engine, metadata = mocked_db_missing_table

        tables_dict = valid_cfg_memory["statement_configs"]["selection"]
        joins = valid_cfg_memory["statement_configs"]["joins"]

        with pytest.raises(gdt.KnownException) as excinfo:
            statement = gdt.statement_builder(
                metadata=metadata,
                engine=engine,
                columns_dict=tables_dict,
                join_list=joins,
            )

        assert "specified in config, does not exist in engine." in str(excinfo.value)

    def test_statement_builder_missingcolumn(
        self, mocked_db_missingcol, valid_cfg_memory
    ):

        engine, metadata = mocked_db_missingcol

        tables_dict = valid_cfg_memory["statement_configs"]["selection"]
        joins = valid_cfg_memory["statement_configs"]["joins"]

        with pytest.raises(gdt.KnownException) as excinfo:
            statement = gdt.statement_builder(
                metadata=metadata,
                engine=engine,
                columns_dict=tables_dict,
                join_list=joins,
            )

        assert "specified in config, does not exist in table" in str(excinfo.value)
