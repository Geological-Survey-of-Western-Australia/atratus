Logging and Exceptions
======================

In data harmonisation tools, we expect to encounter a host of errors associated with the exceptionally diverse data we work with. Each data set has its own unique edge cases and harmonising decades of cross-disciplinary data is by no means an easy task. To achieve this part of our team's work will be codifying the process of parsing files into harmonised databases. In many cases these exceptions should not stop the operation of the system as a whole.

Overview
--------

**There are two main ideas this part of the code is trying to capture:** 

 1. How do we ensure that when the codebase encounters a known edge case it continues or exits gracefully? 
 2. How do we ensure that issues with data and code are easily distinguished and passed to the relevant authority (Subject Matter Expert/Developer)?

The **first** of these issues is handled by mapping the data-associated fault to a *KnownException* and custom message targeting geoscientists, which is raised as as part of a typical try: except pattern in python. 

The **second** case is handled by the division of logging files into two separate files; a program log which captures unhandled exceptions and a KnownExceptions log file which can be given to a geoscientists to review.


Examples
--------

Below is a general example on how to use the gdt logging methods. Note in the example below we show that the type error captures various perturbations of the issues with the inputs. 

.. code-block:: python

    import geo_digital_tools as gdt

    # initialise the logger
    logger = gdt.use_gdt_logging(name="my_cygnet", log_dir="logs", use_excepthook=True)
    
    # our inputs with a wrong value
    v1 = None
    v2 = 2
        
    try:
        # this is our dummy step
        v3 = v1+v2

    # this is one example of a known and handled exception  
    except TypeError as e:
        # logs to the Known Log File
        logger.info(
                f"KnownException: Inputs for this step are invalid : {v1}, {v2}",
                exc_info=True,
                extra={
                    "process_": "my_cygnet",
                    "step_": "step 1",
                    },
                )
    # this catches any other unhandled exceptions
    except Exception as e:
        # logs to the Unhandled Log File
        logger.info(
                f"Unhandled Exception: Encountered unknown error {e}",
                exc_info=True,
                extra={
                    "process_": "my_cygnet",
                    "step_": "step 1",
                    },
                )
