import json
import sqlalchemy as sqla

from typing import Literal
from pathlib import Path
from pydantic import BaseModel, field_validator

import geo_digital_tools.utils.exceptions as gde


class SQLAConnection(BaseModel):
    dialect: Literal["mssql"]
    driver: Literal["pyodbc"]
    un_var: str
    pw_var: str
    host: Literal["SQLD/DEV"]  # NOTE presently only support a single 'trusted' host
    port: int
    database: str  # NOTE we are likely to have a growing list of supported databse consider adding literal.

    # it is possible to set up more sophisticated validation rules
    @field_validator("database")
    def database_not_blank(cls, v: str) -> str:
        condition = v != ""
        if not condition:
            # NOTE this is currently assuming our connection
            # gde error
            gde.KnownException("Database Name cannot be Blank")
        if condition:
            return v

    def build_connection_str(cls) -> str:
        # if we need to authenticate then we'll pull them from the env variables
        con_str = f"{cls.dialect}+{cls.driver}://@{cls.host}/{cls.database}?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server"
        return con_str


def load_db_config(config_path: Path) -> dict:
    """
    This function handles the parsing of he json file into a dict.
    Args:
        config_path : string to dbconfig file.

    Raises/Logs:
        If file won't load/doesn't exist will raise a known exception.

    Returns:
        dictionary of the form {connection name : {connection params}}
    """

    try:
        f = open(config_path)
        db_config = json.load(f)
    except:
        gde.KnownException("Error loading database config file", should_raise=True)

    return db_config


def vadiate_db_config(parsed_dict) -> list:
    """
    Ensures the loaded connections can create valid SqlAlchemy.Engines.
    This utilised pydantic to validate the keys and accepted vlaues for the connection params.

    Args:
        parsed_dict : dictionary of the form {connection name : {connection params}}

    Raises/Logs:
        Logs Known Exceptions : for any value errors.

    Returns:
        dict of valid connections in the form connection_names : SQLAConnection
    """

    valid_connections = {}

    for connection_name, connection_params in parsed_dict.items():
        # check if all required connection params are present and of the right type
        try:
            con_dict = SQLAConnection(**connection_params)
            valid_connections[connection_name] = con_dict
        except Exception as e:
            gde.KnownException(f"Databse config : {connection_name} enountered {e}")

    # validate all the keys and supported value of the config
    return valid_connections


def remote_database(valid_connections_dict: dict) -> dict:
    """
    Args
        Dictionary of the form {Connectionname : SqlaConnection}

    Returns
        Dictionary of the form {Connectionname : SQLA.Engine}
    """

    engine_dict = {}
    for database_name, SqlaConnectionInstance in valid_connections_dict.items():
        engine = sqla.create_engine(
            SqlaConnectionInstance.build_connection_str(), pool_pre_ping=True
        )
        engine_dict[database_name] = engine

    return engine_dict
