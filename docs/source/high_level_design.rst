High Level Design
=================

This section covers where the geo digital toolkit sits in the overal
domain specific ETL processing.

.. |A High level overview| image:: ../assets/tchaikovsky.svg
   :alt: High level overview
   :width: 80%

|A High level overview|


.. note::

      THIS DOESN’T Render in Devops, but does in Sphinx.


Repo Structure
--------------

::

   GDI_GEODIGITAL
   ├── configs                            ] Example configuration files to define a database connection and its schema
   ├── docs                               ┐ Package documentation
   │   └── getting_started_developer.md   |
   │   └── high_level_design.md           │
   │   └── installation_and_use.md        │
   │   └── logging.md                     │
   ├── LICENSE                            │
   ├── README.md                          ┘
   ├── pyproject.toml                     ┐ Package metadata and build 
   ├── .gitignore                         |
   ├── pipelines/                         ┘
   ├── src                                ┐
   │   └── geo_digital_tools              │
   │       ├── __init__.py                │ Package source code
   │       ├── database.py                │
   |       ├── utils                      |
   │       |      ├── __init__.py         |
   │       |      ├── exceptions.py       |
   │       |      ├── statements.py       |
   │       |      └── logging.py          |
   │       └── storage*                   ┘
   └── tests                              ┐
         └── unit                         |
               ├── test_database.py       | Package tests
               ├── test_statement.py      |
               └── test_utils.py          ┘
                     

Architecture
------------

The geodigitaltoolkit is intended to have 3 core modules. 

- database 
      - intended to handle any flavour of sql operations. 
- utils 
      - intended to handle internally known exceptions. 
      - logging operations 
- storage \* 
      - a future extension that will handles connections and file handling operations 
      - moving files, blob storage, file streams etc

--------------

Related Projects
----------------

| All systems we build in this space do so with a single goal.
| Loading data to centralised ‘cleaned’ location.

**Systems and Tools**

- Tchaikovsky : Orchestration, Loadbalancing, Resource Creation\* 
- Atratus : File Classification 
- Cygnets : Domain Specific Transformation and Load

**Outputs**

- Geo Digital : Centralised Respository for all Data 
- Monitoring Dashboard : Centralised Dashboard for all Errors

Futures
-------

In future modules will be built to better characterise the curated data
products produced by the cygnets for the characterisation of the Data
for ML applications.

