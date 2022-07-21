.. _ref_contributing:

============
Contributing
============
Overall guidance on contributing to a PyAnsys library appears in the
`Contributing <https://dev.docs.pyansys.com/how-to/contributing.html>`_ topic
in the *PyAnsys Developer's Guide*. Ensure that you are thoroughly familiar with
this guide, paying particular attention to the `Coding Style
<https://dev.docs.pyansys.com/coding-style/index.html#coding-style>`_ topic, before
attempting to contribute to PyFluent.
 
The following contribution information is specific to PyFluent.

Cloning the PyFluent repository
-------------------------------
Run this code to clone and install the latest version of PyFluent in development
mode:

.. code::

    git clone https://github.com/pyansys/pyfluent.git
    cd pyfluent
    pip install pip -U
    pip install -e .

Building documentation
----------------------
In the root directory of the repository, you can build documentation
locally with:

.. code:: 

    pip install -r requirements/requirements_doc.txt
    cd doc
    make html

After the build completes, the HTML documentation is located in the
``_builds/html`` directory. You can load the ``index.html`` file in
this directory into a web browser.

You can clear all HTML files from the ``_builds/html`` directory with:

.. code::

    make clean

Posting issues
--------------
Use the `PyFluent Issues <https://github.com/pyansys/pyfluent/issues>`_ page to
submit questions, report bugs, and request new features.


Adhering to code style
----------------------
PyFluent is compliant with the `PyAnsys Development Code Style Guide
<https://dev.docs.pyansys.com/coding_style/index.html>`_. It uses the tool
`pre-commit <https://pre-commit.com/>`_ to check the code style. You can
install and active this tool with:

.. code:: bash

   python -m pip install pre-commit
   pre-commit install

You then use the ``style`` rule defined in ``Makefile`` with:

.. code:: bash

   make style

Or, you can directly execute `pre-commit <https://pre-commit.com/>`_ with:

.. code:: bash

    pre-commit run --all-files --show-diff-on-failure
