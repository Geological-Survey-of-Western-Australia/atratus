Core Workflow
=============

Overview
--------

Most geodata harmonisation efforts can best be described as a process, comprised as a series of steps, iterating over a large number of inputs. Each of these steps can encounter errors or issues that will need to be addressed by either:

 - Geoscientist - *Reviews the Data*
 - Developer - *Reviews the Code*

This process of data harmonisation has distinct input requirements for each step. Such that if depending steps fail then subsequent steps can't be run. 

Examples
--------
This UML diagram is intended to capture the two key workflows executed as part of gswa_atratus and the implementation of a data harmonisation workflow. 

- The Red : Executing a defined process (Run Time)
- The Green : Defining a new process (Developing Steps)

This captures how systems build with gswa_atratus are expected to function.

.. |UML of Harmonisation Workflow| image:: ../source/_static/assets/gswa_atratus_core_workflow.svg
   :alt: UML Diagram Overview of Data Harmonisation Process in GSWA Atratus
   |UML of Harmonisation Workflow|

