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
To build the PyFluent documentation locally, run the following commands in the root
(``pyfluent``) directory of the repository:

Windows
~~~~~~~

1. Install poppler
    i. Download `Release-24.08.0-0.zip <https://github.com/oschwartz10612/poppler-windows/releases/download/v24.08.0-0/Release-24.08.0-0.zip>`_.
    ii. Unzip `Release-24.08.0-0.zip`.
    iii. Add `<path to..>/Release-24.08.0-0/poppler-24.08.0/Library/bin` to PATH.

2. Execute the following commands:

.. code:: console

    pip install ansys-fluent-core[docs]
    quarto install tinytex --no-prompt --update-path
    cd doc
    set BUILD_ALL_DOCS=1
    set FLUENT_IMAGE_TAG=v25.1.0
    make html

Linux
~~~~~

.. code:: console

    pip install ansys-fluent-core[docs]
    sudo apt-get update
    sudo apt-get install -y poppler-utils
    quarto install tinytex --no-prompt --update-path
    cd doc
    set BUILD_ALL_DOCS=1
    set FLUENT_IMAGE_TAG=v25.1.0
    make html

After the build completes, the HTML documentation is located in the
``_build/html`` directory. You can load the ``index.html`` file in
this directory into a web browser.

You can clear all HTML files from the ``_build/html`` directory with:

.. code::

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
submit questions, bug reports, and feature requests directly pertaining to PyFluent.

Triage guidance: Is the problem in PyFluent or in Fluent?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Follow this checklist to decide where to open a report.

Quick checklist
^^^^^^^^^^^^^^^
- If the behavior concerns Python packaging, installation, import errors,
  or issues specific to Python → open a PyFluent GitHub issue.
- If the issue relates to a particular Fluent physics model, solver behaviour,
  meshing or solver results, or can be reproduced inside Fluent without Python → raise
  it with Ansys (`Support <https://support.ansys.com>`_ or `Developer Forum <https://discuss.ansys.com>`_).

How to check
^^^^^^^^^^^^
1. Try to reproduce inside Fluent without PyFluent:
   - Use Fluent's journaling/recording capability to record your actions as a Scheme (.jou) or TUI script,
     or translate the Python calls into a Scheme journal.
   - Run the recorded Scheme journal (or equivalent TUI commands) directly in Fluent.
   - If the problem reproduces in Fluent with the Scheme/TUI journal, it is almost certainly a Fluent-side issue.
2. If the issue is only visible when using Python (for example, wrong parameter mapping, malformed request sent to Fluent, missing API convenience) it is likely a PyFluent issue.

When to contact which channel
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- Ansys `Support <https://support.ansys.com>`_: product defects affecting simulation correctness, licensing, installation, or if you need formal tracking.
- Ansys `Developer Forum <https://discuss.ansys.com>`_: general Fluent usage questions, workflow discussion, or community help.
- PyFluent `GitHub <https://github.com/ansys/pyfluent/issues>`_: PyFluent installation, packaging, Python API mapping, client-side bugs, examples, or where there is genuine uncertainty.

If you open a PyFluent issue (recommended when unsure), please include:
- PyFluent version, Python version, OS.
- Fluent product/version, and whether running Fluent GUI, batch, or headless.
- Short description of expected vs actual behavior.
- Minimal reproduction steps (Python snippet) and, if available, the equivalent Scheme/TUI journal produced by Fluent.
- Attach logs, error output, screenshots, and a small case/mesh if possible and allowed by your policies.
- Mark clearly if you have already reproduced the issue by running the Scheme/TUI journal in Fluent.
