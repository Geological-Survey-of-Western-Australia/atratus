GSWA Atratus
============

The GSWA Atratus (**gdt**) is designed to handle the diverse Extract, Transform, Load (ETL) processes required to support harmonising geoscience data. 

This package facilitates:
 - Loading tabular data from databases and files.
 - A common approach to logging errors for data and code issues.
 - Abstract base classes for processing pipelines.

The diagram below is intended to help visualise where **gdt** sits in the data ecosystem. The gdt package provides as consistent approach to logging, database interaction, and process definition that will help ensure a consistent approach across the various data harmonisation efforts undertaken by the GSWA.

.. |A High level overview| image:: ../source/_static/assets/gswa_atratus_highlevel.svg
   :alt: High level overview
   :width: 80%

|A High level overview|


.. Seealso::

      **Want to know what's new checkout the** :doc:`changelog`.



Related Projects
----------------

| All systems we build in this space do so with a single goal.
| Loading data to centralised "cleaned" location.

- Skippy   : Downhole Petrophysics (.las file) harmonisation


----------

.. toctree::
   :maxdepth: 1
   :caption: Getting Started:

   installation
   basic_usage

.. toctree::
   :maxdepth: 1
   :caption: Guides:

   core_workflow
   logging_exceptions
   database_configuration

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   api/gswa_atratus
   changelog

.. toctree::
   :maxdepth: 2
   :caption: Project Links

   GitHub Repository <https://github.com/Geological-Survey-of-Western-Australia>
   Issue Tracker <https://github.com/Geological-Survey-of-Western-Australia>

.. 
   automodule:: gswa_atratus
   :members:
   :undoc-members:
   :show-inheritance: