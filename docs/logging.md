<p style="text-align: center;font-size:2em"> Logging and Exceptions </p>

---

At time of writing to build the atratus database over a local file store for **WAMEX** takes approximately 8-10 hours. This is largely tied to disk read write time as .zips are decompressed (in some cases recursively) and cateloged.

As such, a design decision was made to ensure that errors encountered would not fail the entire cateloging process. The module is located in atratus_exception.py, and logging_utils.py.

There are three main ideas this code is trying to capture.
 - How do we ensure that when the codebase encounters an edge case it exits gracefully?
 - How do we ensure that issues with inputs and code are easily distinguished?
 - How do we get rid of the try except boilerplate?

The **first** of these issues is handled by enforcing that every exception raised is logged. Optionally a parameter can be set in the excption class should also break the code flow. If no logging file is initialised in the session that builds the database (common in debugging and feature testing), then the the logs are written to a 'fail_over.log'.

The **second** case is handled by the division of logging files into two categories, CodeErrors, and KnownExceptions. 
 - CodeErrors : As the name suggests this class is raised in otherwise unhandled cases, it is raised via the decorater discussed below. It is unlikely that this class should every be specifically called in code as when you know there's an error it should be handled or converted to ...
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

[Back to Summary](../readme.md)