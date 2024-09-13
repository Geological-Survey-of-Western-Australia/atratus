import json
from pathlib import Path
import sqlalchemy as sqla

import geo_digital_tools.utils.exceptions as gdte

class ColumnBuilder:
    '''
    Note that for the most part we should use the CamelCase Classes as they are database Agnostic.
    https://docs.sqlalchemy.org/en/20/core/type_basics.html#the-camelcase-datatypes

    Down the line if we opt to support other SQL tyes (such as ARRAY).
    We will need to consider a method for each flavour of SQL.

    I've selectively removed some supported camelcase types typically to reduce complext.
    Consider the case of date, SqlAlchemy supportes, Date, Time, and DateTime.
    My preference is to force a full date time wherever possible (even if we end up with a number of entries at midnight ;).

    #TODO should work out what to do if the config fails for a given column, do we skip it and the related load? or fail build?
    '''
    def __init__(self, columns_json : dict= {}):
        self.columns_json = columns_json
        self.supported_types = {
            'BigInteger' : sqla.BigInteger,
            'Boolean' : sqla.Boolean,
            'DateTime' : sqla.DateTime,
            'Double' : sqla.Double,
            'Enum' : sqla.Enum,
            'Float' : sqla.Float,
            'Integer' : sqla.Integer,
            'LargeBinary' : sqla.LargeBinary,
            'Numeric' : sqla.Numeric,
            'PickleType' : sqla.PickleType,
            'String' : sqla.String,
            'Text' : sqla.Text,
            'UnicodeText' : sqla.UnicodeText,
            'Uuid' : sqla.Uuid,
        }
        self.columns = self.build()
    
    def build(self) -> tuple[sqla.Column]:
        cols = []
        for key, value in self.columns_json.items():
            if value not in list(self.supported_types.keys()):
                gdte.KnownException(f'Parsing Table Encountered Unsupported Type {key} of type {value}')
            else:
                cols.append(sqla.Column(key,self.supported_types[value]))

        return tuple(cols)


def parse_database_config(config_path : Path):
    # this function is a placeholder for a few differnet functions

    # make an engine
    # this will be imported from connect
    engine = sqla.create_engine("sqlite://", echo=True)
    meta = sqla.MetaData()

    # NOTE from here down is what i imagine the function should do
    # these will be jsons we define
    config = json.loads(config_path)

    for table_name, columns_json in config:
        columns = ColumnBuilder(columns_json=columns_json).columns
        table = sqla.Table(table_name, meta, *columns)

    # create all the tables in the associated db
    meta.create_all(engine)

