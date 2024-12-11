"""Abstraction for database operations using SQLAlchemy"""

import sqlalchemy

# Global metadata store within GDI
# See https://docs.sqlalchemy.org/en/20/tutorial/metadata.html
METADATA = sqlalchemy.MetaData()
