Intended Usage
==============

This tool is used to define interfaces between the various projects of
the GDI team. It also handles certain utility functions such as logging
and exception handling.

Installation
------------

Most tools our team develop will ultimately take the form of python
packages that can be installed from internal package repositories.

For access contact gdi.contact@demirs.wa.gov.au. Once access is granted
installation is as easy as.

.. code-block:: shell

   pip install geo_digital_tools

Usage
-----

For the geodigital tool kit there are presently two main use cases: 

- Defining an remote interface between a project and an SQL database. 
  
  - read or write 

- Logging and capturing errors as part of developmenet or data issues.


Both of these use cases are demonstrated in the example script
:file:`example.py`.

:: 
  
  **Exceptions**

  In our code we broadly have two types of errors: those we expect and
  those we don't expect.

  To streamline how these exceptions are encountered, handled, and logged,
  we use a standard logging system to redirect KnownException to a Known Exceptions log file.

  The convenience here is that these two ways of invoking effectively log
  the errors into one of two log files to streamline debugging.

  Lets consider a scenario where we're loading and processing a thousand
  files. We write a function to load the file processing_step_1() and a
  function that does some task with the loaded file processing_step_2().

  .. code-block:: python

    from geo_digital_tools import use_gdt_logging

    def Step_1(file):
      try:
        load_file()
      ....

      # handling known issues
      except issue_1:
        logger.info("KnownException: This file fails {file} - issue_1')
      except issue_2:
        logger.info("KnownException: This file fails {file} - issue_2')
      else:
        break/quit/continue as required.

      return(file_object)

In the two functions above you can see that my first processing step has
already started to map out some known issues with loading the file.

Lets consider the main part of the script below.

.. code:: python

  if __name__=='__main__':
    # 1.
    logger = gdt.use_gdt_logging(name="cygnet_skippy", log_dir="logs", use_excepthook=True)
    
    # define Steps
    step_0 = cygnet.Step_1("Step_1_Open", save=True)
    step_1 = cygnet.Step_2("Step_2_Transform", save=True)
    step_2 = cygnet.Step_3("Step_3_Integrate", save=True)
  
    cygnet_process = cygnet.Process("cygnet_process", input_=_input)
    cygnet_process.addstep(step=step_0)
    cygnet_process.addstep(step=step_1)
    cygnet_process.addstep(step=step_2)

    result = cygnet_process.run()


**So what's interesting about the code above?**

- 1. We configured logging that creates a KnownException logfile using one line.
Any KnownExcpetions will be logged to a seperate file.
Any exceptions encountered but not handled will also be logged using use_excepthook. 
- 1. We created a process to handle our original data input and contain our steps.
The data input will be passed between steps, getting transformed along the way.
- 1. We run the process pipeline using Process.run()


**Why would we want this?**

- It will allow us to characterise multiple issues in larger numbers of files and prioritise fixes:
  
  - i.e. you'll know if the error is encountered once or 300 times based on the logs.

- It allows us to characterise issues in downstream tasks.
  
  - This makes it easier to determine if the issue is caused by a prior step.

- It ensures all exceptions are logged, improving transparency and making edge cases easier to understand.


For more information on how they can be effectively can be used consider
to raise exceptions, and continue on to logging.rst.

