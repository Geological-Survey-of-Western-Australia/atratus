Basic Usage
=============================================

So you're ready to take on geo-data harmonisation! Great how do you get started? 

Now is a great time to talk at a high level about three common problems in geodata harmonisation and how GDT solves them. 

These are:
 - How to implement data harmonisation with a consistent approach
 - Distinguishing between **Data Problems** and **Code Problems**
 - Performing data retrieval from structured databases

Data harmonisation
----------
Geo-data harmonisation involves the correction of meta data, data measurements, and user input in large legacy collections of similar data. These issues arise largely due to variation in industry practice and human factors. We address this with a submodule internally referred to as a cygnet.

In **GDT** the data harmonisation process is broken into two concepts:
 - **Step** - A single operation or transformation done to a set of inputs.
 - **Process** - A series of steps.

----------

Now a Step has a specific set of inputs required to execute a specific set of operations. **GDT** implements this as an abstract base class with methods intended to be overwritten.

These methods are :
 - `can_handle()` - Defines rules to validate the input.
 - `run()` - Defines the operations applied to the valid inputs.
 - `save_method()` - An optional method to save the output of a given step.


.. Seealso::
    More detail can be found in the api docs :py:class:`geo_digital_tools.cygnet.Step`.

----------

A process is just a series of steps chained together, which again forms another abstract base class that, we approach with the chain of responsibility design. Meaning that for subsequent steps to run prior steps need to be successful.
The class also allows variables relevant to the entire process to be grouped as class variables. As a result it's methods are simply used to add or remove steps and run the process.

These methods are :
 - `addstep()` - Adds a step to the process.
 - `dropstep()` - Removes a step from the process
 - `start()` - Executes the process.


.. Seealso::
    More detail can be found in the api docs :py:class:`geo_digital_tools.cygnet.Process`.


Developers and Geoscientists
----------
Another challenge about geodata harmonisation is the distinguishing between problems that can be solved by a developer and problems that can be solved by a geoscientist. **GDT** handles this by raising two types of exceptions:

 - :py:class:`geo_digital_tools.KnownException` - This Exception is intended to be raised when the cause of the issue/error is known. Ideally this is something that can be explained to a geoscientist to either fix or at least be aware of.
 - :py:class:`geo_digital_tools.CodeError` - This Exception is intended to be raised by any uncaught exceptions, or any issue that a developer needs to consider and discuss. Often it will be used for discovering new edge cases.

These exceptions are 'tagged' and sent to different log files to facilitate user and developer review of the existing data harmonisation workplace.  

Getting data from a Database
----------

Many organisations collate and organise their geoscience data in centralised SQL databases. However the schemas of the databases and flavours of SQL used vary team to team and organisations.
Further many tools used for file parsing are written and maintained in python. Many geoscientists have little familiarity with either of these languages but have a clear understanding of what data they need from the database to perform a given harmonisation task.

As such we need an approach to configure a database requests which is human readable/editable but can be used to retrieve data from a variety of database settings, and delivers it into a python setting.
By using json to define a configuration file, and sqlAlchemy to handle database interaction, we've written a set of functions to select data from a database and return a pd.DataFrame.