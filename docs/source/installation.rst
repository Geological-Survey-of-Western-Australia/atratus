Installation
========================

This package is distributed via the pypi.org so installation is as simple as. 

.. code-block:: shell

   pip install geo_digital_tools

If you're intending to use the utilities in **geo_digital_tools** to do your own data harmonisation workflow we recommend this method of import.

.. code-block:: python
   
   import geo_digital_tools as gdt


Developer Installation
----------

If you're a developer and interested in contributing then we recommend cloning our code base directly from git, and doing any testing and prototyping using the workflow below.

**Editable Installation:**

During the development process, it is essential to ensure that the functionality being prototyped works correctly within the module. This can be achieved using pip's editable install mode.

To set up an editable install, execute the following commands in your terminal within the project directory:

.. code-block:: shell

   # Perform an editable install, which allows the virtual environment to track changes in the source code.
   # This command also installs all package dependencies.
   pip install -e .

We would welcome code changes or documentation improvements or both!
To support this you can install the optional dependencies below by using the following commands:

For Windows users

.. code-block:: shell

   # Install the optional dependencies for code contributions
   pip install .[tests]
   pip install .[dev]
   # Install the optional dependencies for documentation contributions
   pip install .[docs]
   pip install .[docs-extra]

.. Note::
   For Mac users substitute `pip install .[docs-extra]` for **`pip install '.[docs-extra]'`**.
