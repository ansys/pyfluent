.. _ref_contributing:

============
Contributing
============
Overall guidance on contributing to a PyAnsys library appears in the
`Contributing <https://dev.docs.pyansys.com/overview/contributing.html>`_ topic
in the *PyAnsys Developer's Guide*. Ensure that you are thoroughly familiar with
it and all `Guidelines and Best Practices
<https://dev.docs.pyansys.com/guidelines/index.html>`_ before attempting to
contribute to PyFluent.
 
The following contribution information is specific to PyFluent.

Cloning the PyFluent Repository
-------------------------------
Run this code to clone and install the latest version of PyFluent in development
mode:

.. code::

    git clone https://github.com/pyansys/pyfluent.git
    cd pyfluent
    pip install pip -U
    pip install -e .
    pip install -e .[post] # If you want to use pyvista

Building Documentation
----------------------
To build the documentation locally you need to follow these steps at the root
directory of the repository:

.. code:: 

    pip install -r requirements_docs.txt
    cd doc
    make html

After the build completes the html documentation is located in the
``_builds/html`` directory and you can load the ``index.html`` into a web
browser.  To clean the documentation you can execute this command:

.. code::

    make clean

Posting Issues
--------------
Use the `PyFluent Issues <https://github.com/pyansys/pyfluent/issues>`_ page to
submit questions, report bugs, and request new features.


Code Style
----------
PyFluent is compliant with `PyAnsys Development Code Style Guide
<https://dev.docs.pyansys.com/coding_style/index.html>`_.  Code style is checked
by making use of `pre-commit <https://pre-commit.com/>`_. Install this tool and
activate it executing the following commands:

.. code:: bash

   python -m pip install pre-commit
   pre-commit install

Then, you can use the ``style`` rule defined in the ``Makefile``:

.. code:: bash

   make style

Or directly execute `pre-commit <https://pre-commit.com/>`_:

.. code:: bash

    pre-commit run --all-files --show-diff-on-failure
