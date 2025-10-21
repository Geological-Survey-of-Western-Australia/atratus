Database Configuration
======================

Many organisations as part of internal processes load their various geoscience relevant metadata into internal databases. 

Geoscientists that review and ultimately use geodata products; are mostly unfamiliar with the structure of the SQL backend. This can create communication issues between users and DB admins who can provide the database extracts or views needed to complete geodata harmonisation workflows. 

Overview
--------

Here we define a preliminary structure that is intended to act as a tool to define this interface to support automated extraction from SQL databases. This means that users can create a config file that can be easily read and edited by a geoscientist. 

We use `SQLAlchemy <https://www.sqlalchemy.org/>`_  to translate these configs to select statements that can be on databases built with different SQL technologies (t-SQL, ms-SQL etc.).

Examples
--------

To define your first gdt database config lets consider the various keys and their values:

- **sqlalchemy** - This specifies how sqlalchemy will connect to the database.
    - *Ask your DBA for a connection string/url.*
- **statement_configs** - This specifies the tables you want to retrieve and how they'll be joined.
    - **selection** - defines which tables and columns we're wanting to select. 
    - **joins** - defines join behaviour between two tables
    - **aliases** - defines a mapping from one table name to another (useful when backend table names are confusing to users.)

.. Note::
    Note most errors that could reasonably be encountered when creating this config (such as specifying a column that isn't in a table), will be raised as errors when the config is loaded. See the API reference :py:class:`geo_digital_tools.load_statement`.

.. literalinclude:: _static\assets\_example_cfg.json
   :language: json
   :caption: Example GDT-DB Config File