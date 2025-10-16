Basic Usage
=============================================

So you're ready to take on geo-data harmonisation! Great how do you get started? 

Now is a great time to talk at a high level about three common problems in geodata harmonisation and how GDT solves them. 

These are:
 - How to implement data harmonisation with a consistent approach
 - Distinguishing between **Data Problems** and **Code Problems**
 - Perfomring data retrieval from structured databases

Data harmonisation
----------
Geo-data harmonisation involves the correction of meta data, data measurments, and user input in large legacy collections of similar data. These issues arise largely due to variation in industry practice and human factors. We adress this with a submodle internally refered to as a cygnet.

In **GDT** the data harmonisation process is broken into two concepts:
 - **Step** - A single operation or transformation done to a set of inputs.
 - **Process** - A series of steps.

----------

Now a Step has a specific set of inputs required to execute a specific set of operations. **GDT** implements this as an abstract base class with methods intended to be overwritten.

These methdods are :
 - `can_handle()` - Defines rules to validate the input.
 - `run()` - Defines the operations applied to the valid inputs.
 - `save_method()` - An optional method to save the output of a given step.


.. Seealso::
    More detail can be found in the api docs :py:class:`geo_digital_tools.cygnet.Step`.

----------

A process is just a series of steps chained together, which again forms another abstract base class that, we approach with the chain of responsibility design. Meaning that for subsequent steps to run prior steps need to be successful.
The class also allows variables relevant to the entire process to be grouped as class variables. As a result it's methods are simply used to add or remove steps and run the process.

These methdods are :
 - `addstep()` - Adds a step to the process.
 - `dropstep()` - Removes a step from the process
 - `start()` - Executes the process.


.. Seealso::
    More detail can be found in the api docs :py:class:`geo_digital_tools.cygnet.Process`.


Developers and Geoscientists
----------


Getting data from a Database
----------