Logging and Exceptions
======================

In analytical systems like those we build in our team, we expect to
encounter a host of errors associated with the exceptionally diverse
data we work with. Each data set has its own unique edge cases and
harmonising decades of cross-disciplinary data is by no means an easy
task. To achieve this part of our team's work will be codifying the
process of parsing files into harmonised databases. In many cases these
exceptions should not stop the operation of the system as a whole.

**There are three main ideas this code is trying to capture：** 

1. How do we ensure that when the codebase encounters a known edge case it continues or exits gracefully? 
1. How do we ensure that issues with inputs and code are easily distinguished? 
1. How do we get rid of the try:except boilerplate?

The **first** of these issues is handled by logging every data-associated fault with a *KnownException*.
Faults with the codebase may cause the program to exit per normal.

The **second** case is handled by the division of logging files into two
categories, a program log and KnownExceptions. 

- **KnownException** : Once an error is discovered it's cause determined. A decision needs to be made to decide if the case in question should be handled by the code base. If so a card should be raised detailing the issue and adding a card to the backlog.

The **third** of these issues is addressed using a exception handler, which logs unhandled exceptions.

In general, a standard logging setup can be enabled by running the configuration function as follows:

.. code:: python
    logger = gdt.use_gdt_logging(name="my_cygnet", log_dir="logs", use_excepthook=True)

Overview
----------------------



Examples
----------------------
