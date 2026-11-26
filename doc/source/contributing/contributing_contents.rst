.. _ref_contributing:

========================
Contributing to PyFluent
========================

.. toctree::
   :maxdepth: 1
   :hidden:

   environment_variables

General guidance on contributing to a PyAnsys library appears in the
`Contributing <https://dev.docs.pyansys.com/how-to/contributing.html>`_ topic
in the *PyAnsys Developer's Guide*. Ensure that you are thoroughly familiar with
this guide, paying particular attention to the `Coding Style
<https://dev.docs.pyansys.com/coding-style/index.html#coding-style>`_ topic, before
attempting to contribute to PyFluent.
 
The following contribution information is specific to PyFluent.

Clone the repository
--------------------
Follow the steps in the Development Installation section of :ref:`ref_installation` 
to set PyFluent up in development mode.

Run unit tests
--------------

To run the PyFluent unit tests, execute the following command in the root
(``pyfluent``) directory of the repository:

.. code:: console

    pip install ansys-fluent-core[tests]
    python -m pytest -n 4 --fluent-version=25.1

You can change the Fluent version by replacing ``25.1`` with the version you want to test.

Build documentation
-------------------
The documentation can be built locally without a Fluent installation, API
codegen, ``quarto``, or poppler. Install the documentation dependencies and
run the HTML build from the ``doc`` directory of the repository:

.. code:: console

    pip install ansys-fluent-core[docs]
    cd doc
    set PYFLUENT_DOC_SKIP_CHEATSHEET=1
    make html

On Linux and macOS, use ``export PYFLUENT_DOC_SKIP_CHEATSHEET=1`` instead of
``set``. The cheat sheet is the only part of the documentation that needs
poppler, which converts its PDF output to PNG. The examples gallery is not
executed during a local build, so no Fluent session is needed.

The HTML documentation is written to ``_build/html``. Open its
``index.html`` file in a browser to view it.

To include the parts that need extra setup, set these variables before
running ``make html``:

* ``BUILD_ALL_DOCS=1`` generates the settings, datamodel, and TUI API
  reference pages. When it is unset, these generation scripts are skipped
  and the remaining pages are built without generated API files. To use
  it, the generated API files must exist. On a fresh clone, generate them
  with ``python codegen/allapigen.py``, which requires a licensed Ansys
  Fluent installation. See the Development Installation section of
  :ref:`ref_installation`.

* ``FLUENT_IMAGE_TAG`` selects the Fluent version whose generated API files
  are used for the settings API reference. It is the tag of the Fluent
  Docker image that PyFluent uses when launching in a container; for
  example, ``v25.1.0`` selects the files in
  ``src/ansys/fluent/core/generated/v251``. When it is unset, PyFluent uses
  the latest released Fluent version, so you do not need to set it if that
  version matches your generated API files. See
  :ref:`ref_environment_variables`.

* ``PYFLUENT_DOC_SKIP_EXAMPLES=1`` omits the examples gallery.

To build the cheat sheet as well, install poppler and the ``quarto`` PDF
toolchain, and leave ``PYFLUENT_DOC_SKIP_CHEATSHEET`` unset.

Windows
~~~~~~~

1. Download `Release-24.08.0-0.zip <https://github.com/oschwartz10612/poppler-windows/releases/download/v24.08.0-0/Release-24.08.0-0.zip>`_ and unzip it.
2. Add ``<path to>/Release-24.08.0-0/poppler-24.08.0/Library/bin`` to ``PATH``.

Linux
~~~~~

.. code:: console

    sudo apt-get update
    sudo apt-get install -y poppler-utils

On both platforms, install ``tinytex`` and build the documentation:

.. code:: console

    quarto install tinytex --no-prompt --update-path
    cd doc
    make html

You can clear all generated HTML files from ``_build/html`` with:

.. code:: console

    make clean

Adhere to code style
--------------------
PyFluent is compliant with the `PyAnsys code style
<https://dev.docs.pyansys.com/coding-style/index.html>`_. It uses the tool
`pre-commit <https://pre-commit.com/>`_ to check the code style. You can
install and activate this tool with:

.. code:: bash

   python -m pip install pre-commit
   pre-commit install

You can then use the ``style`` rule defined in ``Makefile`` with:

.. code:: bash

   make style

Or, you can directly execute `pre-commit <https://pre-commit.com/>`_ with:

.. code:: bash

    pre-commit run --all-files --show-diff-on-failure

In order to have a nice :ref:`ref_release_notes` section, it is important to follow
the branch and commit names conventions as described in the *PyAnsys Developer's Guide*
`branch <https://dev.docs.pyansys.com/how-to/contributing.html#branch-naming-conventions>`_ and 
`commit <https://dev.docs.pyansys.com/how-to/contributing.html#commit-naming-conventions>`_ naming
sections.

Post issues
-----------
Use the `PyFluent Issues <https://github.com/ansys/pyfluent/issues>`_ page to
submit bug reports and feature requests directly pertaining to PyFluent.

Triage guidance
~~~~~~~~~~~~~~~
Follow this checklist to decide whether the issue belongs to PyFluent or Fluent:

- If the issue relates to a particular Fluent physics model, solver behavior,
  meshing or solver results, or can be reproduced inside Fluent without Python → raise
  it with (`Ansys customer support <https://support.ansys.com>`_ or `Ansys developer forum <https://discuss.ansys.com>`_).
- If the behavior concerns Python packaging, installation, import errors,
  or issues specific to PyFluent → open a PyFluent GitHub issue.
