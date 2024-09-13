<p style="text-align: center;font-size:2em"> Logging and Exceptions </p>

---

In analytical systems like those we build in our team, we expect to encounter a host of errors associated with the exceptionally diverse data we work with. Each data set has its own unique edge cases and harmonising decades of cross-disciplinary data is by no means an easy task. To achieve this part of our team’s work will be codifying the process of parsing files into harmonised databases. In many cases these exceptions should not stop the operation of the system as a whole. 

There are three main ideas this code is trying to capture.
 - How do we ensure that when the codebase encounters a known edge case it exits gracefully?
 - How do we ensure that issues with inputs and code are easily distinguished?
 - How do we get rid of the try except boilerplate?

The **first** of these issues is handled by enforcing that every exception raised is logged. Optionally a parameter can be set in the exception class should also break the code flow. If no logging file is initialised in the session that builds the database (common in debugging and feature testing), then the logs are written to a 'fail_over.log'.

The **second** case is handled by the division of logging files into two categories, CodeErrors, and KnownExceptions. 
 - CodeErrors : As the name suggests this class is raised in otherwise unhandled cases, it is raised via the decorator discussed below. It is unlikely that this class should every be specifically called in code as when you know there's an error it should be handled or converted to ...
 - KnownException : Once an error is discovered it's cause determined. A decision needs to be made to decide if the case in question should be handled by the code base. If so a card should be raised detailing the issue and adding a card to the backlog.  

The **third** of these issues is addressed using the exception handler pseudo decorator, when new functionality is being developed. 



```python 
# case 1
@exception_handler()
def my_bad_unimportant_function():
    silly = {}
    print(silly['Billy']) --> this will raise a KeyError

# execution
> my_bad_unimportant_function() --> logs and fails quietly
> my_other_function() --> this will run

# case 2
@exception_handler(should_break=True)
def my_bad_super_critical_function():
    silly = {}
    print(silly['Billy']) --> this will raise a KeyError

# execution
> my_bad_super_critical_function() --> logs and slams on the breaks
> my_other_function() --> this will NOT run
```

---
# Azure App Insights
At this stage of the project I consider it likely that we'll move towards having our applications logs being sent to an azure interface somewhere.
This will likely take the form of an azure app insights, we'll want to keep a 'local' copy of our logs to facilitate testing and development. However, as our services enter production it will be useful to have a dash to monitor the issues we're hitting.

Fortunately Azure App Insights is designed with this in mind. [The documentation](https://learn.microsoft.com/en-us/previous-versions/azure/azure-monitor/app/opencensus-python) and it's as simple as adding a handler to the python logger class.

```python 
import logging

from opencensus.ext.azure.log_exporter import AzureLogHandler

logger = logging.getLogger(__name__)
logger.addHandler(AzureLogHandler())
# Alternatively manually pass in the connection_string
# logger.addHandler(AzureLogHandler(connection_string=<appinsights-connection-string>))

properties = {'custom_dimensions': {'key_1': 'value_1', 'key_2': 'value_2'}}

# Use properties in logging statements
logger.warning('action', extra=properties)
```

We currently implement this by having a this using the deployed variable in our setup_logger() function. The advised docs specify adding an environemental variable for connection for app insights connections. 

We'll have to have a think about how we do this as part of deployment and how we'll need to convey the source library (i.e. which project is logging the error) of the error via the logging module.

In summary the setuplogger function and the associated exceptions (that log to them) will need to be refactored once we get to that point so that app-insights gives usefully easily parsed info.

```
APPLICATIONINSIGHTS_CONNECTION_STRING=<appinsights-connection-string>
```

```python 
def setup_logger(
    name: str,
    log_file: Path,
    level: int = 10,
    logging_format: str = "%(asctime)s %(levelname)s %(message)s",
    deployed : bool = False
) -> logging.Logger:
    """
    Generates a logger and specifies the formatting.
    """
    formatter = logging.Formatter(logging_format)
    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    
    if deployed:
        logger.addHandler(AzureLogHandler()
                          )

    return logger
```

[Back to Summary](../readme.md)