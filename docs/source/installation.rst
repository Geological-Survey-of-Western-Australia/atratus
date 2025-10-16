Installation
========================


**Standard Installation:**

This package is distributed via the pypi.org 
.. code-block:: shell

    pip install geo_digital_toolkit

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

If you encounter any issues 
