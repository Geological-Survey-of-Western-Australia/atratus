## GDI - GeoDigitalToolkit

*A Common Toolkit for Data Handling*
___

All digital geoscience data requires extremely diverse ETL processes. While the extraction and transformation processes require highly bespoke solutions (cygnets), the loading of data is often performed with general-purpose tools. 

This library is designed to facilitate the loading of tabular data from various projects. The goal is to centralise the data handling tools and logging, to facilitate loading datasets into a single structured database.  In addition to loading extracted data into databases, internal data stores can be read and defined via the Interface class. This allows for a consistent approach to database interactions. We follow a Connect, Create, Read, Update, and Delete (CCRUD) approach to database operations.

This system is intended purely for internal usage by GSWA personnel, for reading and loading various tabular outputs. 

## Feature List
 - Basic database operations (SQL)
 - Error Logging and Handling
 - Storage Operations (Blob/Local)*

## Documentation
- [Getting Started for Developers](docs/source/getting_started_developer.rst)
- [General Design & Flow](docs/source/high_level_design.rst)
- [Installation and Use](docs/source/installation_and_use.rst)
- [Logging](docs/source/logging.rst)