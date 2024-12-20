<p style="text-align: center;font-size:2em"> Intended Usage </p>

---
This tool is used to define interfaces between the various projects of the GDI team. It also handles certain utility functions such as logging and exception handling. 

### Installation
Most tools our team develop will ultimately take the form of python packages that can be installed from internal package repositories. 

For access contact gdi.contact@demirs.wa.gov.au. Once access is granted installation is as easy as.
~~~ py
pip install geo_digital_tools
~~~

### Usage
For the geodigital tool kit there are presently two main use cases:
- Defining an remote interface between a project and an SQL database.
   - read or write
- Logging and capturing errors as part of developmenet or data issues.

Both of these use cases are demonstrated in the example script `example.py`.

```

**Exceptions**

In our code we broadly have two types of errors: those we expect and those we don't expect.

To streamline how these exceptions are encountered, handled, and logged, we use our gde exeptions in one of two ways:
-  The exception_handler decorator 
-  Calling the gde.KnownException function.

The convenience here is that these two ways of invoking effectively log the errors into one of two log files to streamline debugging.

Lets consider a scenario where we're loading and processing a thousand files. We write a function to load the file processing_step_1() and a function that does some task with the loaded file processing_step_2().



```python
from geo_digital_tools import exception_handler, KnownException

@exception_handler()
def processing_step_1(file):
    file_object = None
    # try to load file
    ....

    # handling known issues
    if issue_1:
        KnownException(f'This file fails {file} - issue_1')
    if issue_2:
        KnownException(f'This file fails {file} - issue_2')

    return(file_object)

@exception_handler()
def processing_step_2(file_object):
    # some fancy processing code being prototyped
    ....

    return(final)
```

In the two functions above you can see that my first processing step has already started to map out some known issues with loading the file. You'll also see that I've decorated both my functions with the exception handler, here any uncaught exceptions will be passed into my code issues log file.

Lets consider the main part of the script below.

``` python
if __name__=='__main__':

    # a big list of files we're trying to load
    files = [.....] 
    final_outputs = []

    # iterating through the list
    for file in files:
        file_object = processing_step_1(file) 
        if file_object != None:
            final_object = processing_step_2(file) 
            final_outputs.append(final_object)

    print('completed')
```
So what's interesting about the code above?
- First : Every file will attempt processing_step_1 regardless of any exceptions encounterd.
- Second : Any KnownExcpetions will be logged to a seperate file.
- Third : Any exceptions encountered in processing step 2 will also be logged.
- Fourth : the print statement will always be executed.

Why would we want this? 
- It will allow us to characterise multiple issues in larger numbers of files and prioritise fixes:
    - i.e. you'll know if the error is encountered once or 300 times based on the logs.
- It allows us to characterse issues in downstream tasks.
    - this makes it easier to determine if the issue is caused by a prior step.
- It ensures all exceptions are logged improving transparency and making edge cases easier to understand.

For more information on how they can be effectively can be used consider the should_raise argument and the logging.md

---

[Back to Summary](../readme.md)