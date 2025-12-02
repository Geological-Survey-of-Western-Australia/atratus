GSWA Atratus
============

The GSWA Atratus (**gdt**) is designed to handle the diverse Extract, Transform, Load (ETL) 
processes required to support harmonising geoscience data.

This package provides:

- Loading tabular data from databases and files.
- A common approach to logging errors for data and code issues.
- Abstract base classes for processing pipelines.

The diagram below illustrates where **gdt** sits in the data ecosystem. It provides consistent
approaches to logging, database interaction, and process definition—supporting the various data
harmonisation efforts undertaken by GSWA.

.. |high_level_overview| image:: _static/assets/gswa_atratus_highlevel.svg
   :alt: High level overview
   :width: 80%

|high_level_overview|

.. seealso::

   Want to know what's new? Check out the :doc:`changelog`.

Related Projects
----------------

All systems we build in this space aim to achieve a single goal:
loading data into a centralised, "cleaned" location.

**Skippy**

Downhole Petrophysics (.las file) harmonisation


.. toctree::
   :maxdepth: 1
   :caption: Getting Started

   installation
   basic_usage

.. toctree::
   :maxdepth: 1
   :caption: Guides

   core_workflow
   logging_exceptions
   database_configuration

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   autoapi/index
   changelog
   contributing

.. toctree::
   :maxdepth: 1
   :caption: Project Links

   GitHub Repository <https://github.com/Geological-Survey-of-Western-Australia/atratus>
   Issue Tracker <https://github.com/Geological-Survey-of-Western-Australia/atratus/issues>
