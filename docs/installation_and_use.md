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

Both of these use cases have an example below.

**Interface Definition**
```python 
from sqlalchemy.sql.expression import Select as Select
import sqlalchemy as sqla
from pathlib import Path

import geo_digital_tools.utils.exceptions as gde
import geo_digital_tools.database.connect as connect
from geo_digital_tools.database.read import ReadInterface

# here we define one interface our project uses however there could be many
class MyInterface(ReadInterface):
    def __init__(self, engine):
        super().__init__(engine)

    def select_statement(self):
        # we overwrite the base class selction function
        stmt = sqla.Select()

        tables_valid = False
        try:
            view_1 = sqla.Table("TABLE1", sqla.MetaData(), autoload_with=self.engine)
            view_2 = sqla.Table("TABLE2", sqla.MetaData(), autoload_with=self.engine)
            tables_valid = True

        except sqla.exc.OperationalError as e:

            gde.KnownException(
                f"My Interface : Encountered {e} - Table Does Not Exist",
                should_raise=True,
            )

        if tables_valid:
            # make our statement note Id and Name are columns in those tables
            try:
                stmt = sqla.select(view_1.c.Id, view_1.c.Name, view_2.c.Name).join(
                    view_2, view_1.c.Id == view_2.c.Id
                )
            except AttributeError as e:
                gde.KnownException(
                    f"My Interface : Encountered {e} - Column Not Present in Table"
                )

        return stmt


if __name__ == "__main__":

    config_con_path = Path("db_connection_config.json")

    # load connections for your project
    config_json = connect.load_db_config(config_con_path)
    config_valid = connect.validate_db_config(config_json)
    config_cons = connect.remote_database(config_valid)

    # Create and retrieve your interface
    example = MyInterface(engine=config_cons["config_key"])
    example.validate_interface()
    example.get_interface()
    print(example.interface_to_df())


```

**Exceptions**

In our code we broadly have two types of errors: those we expect and those we don't expect.

To streamline how these exceptions are encountered, handled, and logged, we use our gde exeptions in one of two ways:
-  The exception_handler decorator 
-  Calling the gde.KnownException function.

The convienience here is that these two ways of invoking: effectively log the errors into one of two log files to streamline debugging.

Lets consider a scenario where we're loading and processing a thousand files. We write a function to load the file processing_step_1() and a function that does some task with the loaded file processing_step_2().



```python
from geo_digital_toolkit.utils.exceptions import exception_handler
import geo_digital_toolkit.utils.exceptions as gde

@exception_handler()
def processing_step_1(file):
    file_object = None
    # try to load file
    ....

    # handling known issues
    if issue_1:
        gde.KnownException(f'This file fails {file} - issue_1')
    if issue_2:
        gde.KnownException(f'This file fails {file} - issue_2')

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