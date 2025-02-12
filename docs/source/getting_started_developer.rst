Developer start up guide
========================

This section covers:
 - Required Downloads
 - Clone the repository locally
 - Setting up a Python Virtual Environment
 - Creating an editable install
 - Running Unit Tests

Downloads
---------

Several programs and downloads are required to access and use the
repository

- Desired IDE/text editor, eg. Visual Studio Code
   - [Download VS Code](https://code.visualstudio.com/download)
   - if you can’t install this raise a service now ticket.

- Python, 3.11 is currently being used within the project 
   - The 64 bit version is required for several of the used packages (Windows)
   - https://www.python.org/downloads
   - if you can’t install this raise a service now ticket.

- Git, required to push/pull/etc git commands
   - https://git-scm.com/downloads

Access
------
In the short term it is likely that access will remain relative to locally provideed harddrives. This is a placeholder for if we move to a live access approach.

- Clone the repository
- Clone the repository locally, this can be done through devops, github desktop or vs code. 

Virtual Environment Setup
-------------------------

**For Windows users:**

Set the execution policy to the current user and the policy to remote
signed.

.. code-block:: shell

   Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned

Create the virtual environment at the location “./venv”

.. code-block:: shell

   python -m venv ./.venv

Activate the virtual environment by navigating to the activate file in
the following location.

.. code-block:: shell

   ./.venv/Scripts/activate

**For Mac users:**

Create the virtual environment at the location “./venv”

.. code-block:: shell

   python3 -m venv ./.venv

Activate the virtual environment by navigating to the activate file in
the following location.

.. code-block:: shell

   source ./.venv/bin/activate


Setting up pip install
-------------------------------

**Standard Installation:**

After activating the virtual environment (you may need to restart VS Code) and navigating to the project directory, install the project using the `pyproject.toml` file.

.. code-block:: shell

    pip install .

**Editable Installation:**

During the development process, it is essential to ensure that the functionality being prototyped works correctly within the module. This can be achieved using pip's editable install mode.

To set up an editable install, execute the following commands in your terminal within the project directory:

.. code-block:: shell

   # Perform an editable install, which allows the virtual environment to track changes in the source code.
   # This command also installs all package dependencies.
   pip install -e .

If you require optional dependencies, use the following commands:

For Windows users

.. code-block:: shell

   # Install the optional dependencies for testing
   pip install .[tests]
   pip install .[dev]
   # Install the optional dependencies for documentation
   pip install .[docs]
   pip install .[docs-extra]

For Mac users：

.. code-block:: shell


   # Install the optional dependencies for testing
   pip install '.[tests]'
   pip install '.[dev]'
   # Install the optional dependencies for documentation
   pip install '.[docs]'
   pip install '.[docs-extra]'

.. note::
   
   If you use Jupyter notebooks during the development process, you may need to restart the kernel periodically to ensure that any changes are loaded into the kernel session.


Unit tests
----------

This project uses the pytest framework for testing and pytest-cov for
coverage reporting. The tests can be run by navigating to the testing
side tab of vscode, or via comandline as below.

.. code-block:: shell

   python -m pytest .\tests\

With the .venv active running the line below generates the coverage
report, which works well with the vscode extension coverage gutters in
watch mode. When used well test coverage can be highly useful in
developing good meaningful test suite.

While it is tempting to aim for high coverage, what is more important is
the development of robust tests that ensure functionality and facilitate
the reliability of the code.

.. code-block:: shell

   pytest --cov-report xml:tests\coverage.xml --cov src\geo_digital_tools
