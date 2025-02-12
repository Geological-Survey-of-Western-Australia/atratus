.. GeoDigitalToolkit documentation master file, created by
   sphinx-quickstart on Thu Oct 14 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


GeoDigitalToolkit
=============================================

*A Common Toolkit for Data Handling*

GeoDigitalToolkit is designed to handle the diverse ETL processes required for digital geoscience data. While extraction and transformation are often project-specific (cygnets), data loading is typically performed with general-purpose tools. 

This library facilitates:
 - Loading tabular data from various projects.
 - Centralized data handling and logging.
 - Integration with structured databases.
 - A consistent approach to database interactions** via the CCRUD (Connect, Create, Read, Update, and Delete) methodology.

This system is intended for internal usage by GSWA personnel to read and load tabular datasets.


Feature List:
 - Basic database operations (SQL)
 - Error Logging and Handling
 - Storage Operations (Blob/Local)


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   getting_started_developer
   high_level_design
   installation_and_use
   logging

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   api/geo_digital_tools

.. 
   automodule:: geo_digital_tools
   :members:
   :undoc-members:
   :show-inheritance: