.. _faqs:

Frequently asked questions
==========================

What is PyAnsys?
----------------
PyAnsys is a set of open source technologies that allow you to interface Pythonically
with Ansys Fluent, Mechanical APDL, AEDT, and other Ansys products. You can use PyAnsys
libraries within a Python environment of your choice in conjunction with external Python
libraries.

.. image:: ../_static/PyAnsys_overview.png
  :width: 800
  :alt: PyAnsys overview

What is PyFluent?
-----------------
PyFluent provides Pythonic access to Ansys Fluent. Its features enable the seamless use of
Fluent within the Python ecosystem and broad access to native Fluent features for performing
actions such as these:

- Launch Fluent using a local Ansys installation.
- Connect to a Fluent instance running on a remote machine.
- Use Fluent's TUI (text user interface) commands for both meshing and solver features.
- Use Fluent's built-in postprocessing capabilities.

PyFluent is bundled with the Fluent installation. You can also download and install PyFluent
separately. For more information, see :ref:`faqs_install`, which appears later on this page.

PyFluent has no GUI (graphical user interface). You interact with PyFluent through the Python
environment of your choice.

How does PyFluent compare to UDFs?
----------------------------------
PyFluent is conceptually aligned with Fluent TUI console commands (and journaling) rather than with
UDFs (user-defined functions). In other words, PyFluent is used for automation rather than
modifying the solver behavior.

UDFs continue to be written in C and remain important elements of
Fluent simulations.

While you cannot write UDFs in Python, you can execute PyFluent commands to compile and load UDFs,
similar to how you use TUI commands.

Who should use PyFluent?
------------------------
PyFluent users include engineers, product designers, consultants, and academia.

.. image:: ../_static/who_why_use_PyFluent.png
  :width: 800
  :alt: PyFluent users and objectives


- Enhance productivity with customized scripts.
- Automate multi-product workflows.
- Extend CFD simulations to a wider audience by creating vertical apps.
- Create comprehensive workflows inspired by Python's increasingly broad offerings
  in these areas of scientific computing:

  - Computer vision
  - ML (machine learning)
  - AI (artificial intelligence)
  - Data processing and visualization
  - Optimization

- Use widely accepted libraries and notations to compute
  multi-dimensional arrays in the Python environment.


.. image:: ../_static/libraries_notations.png
  :width: 800
  :alt: Widely accepted libraries and notations


What can you do with PyFluent?
------------------------------
You can use PyFluent to do tasks such as these:

- Integrate Fluent as a solver seamlessly in your in-house design tools.
- Customize postprocessing, perhaps by using Python's vast external
  library to extend postprocessing capabilities or by automatically generating
  a PowerPoint presentation to show simulation results.
- Use a web app to access jobs running on a cluster, monitor convergence, and
  generate graphs.
- Leverage ML and AI, especially for models that are solved quickly but can be
  improved as additional knowledge is acquired and applied.
- Use Python APIs to couple different Ansys products.

.. _faqs_install:

How do you install PyFluent?
----------------------------
While :ref:`installation` provides basic information for quickly
installing and launching the ``ansys-fluent-core`` package, these
steps explain how to install all PyFluent packages in a Python *virtual
environment*:

#. Install Python if it is not already installed.

   For Python version information, see the answer to the next question.

#. Install Fluent 2022 R2 or later.
#. Set the environment variable for your installed release to point to
   the appropriate Ansys installation folder.
   
   For example, for Ansys 2022 R2, you would likely set the ``AWP_ROOT222``
   environment variable to point to ``C:\Program Files\ANSYS Inc\v222``.

   While you must explicitly set this environment variable on Linux, it should
   be automatically set on Windows.

#. In a command window, use this code to set up and activate a local Python
   virtual environment::
      
    python -m venv pyenv   # Set up a local virtual environment
    pyenv\Scripts\activate   # Activate the virtual environment on Windows
    source pyenv/bin/activate.csh   # Activate the virtual environment on Linux (csh)
    . pyenv/bin/activate   # Activate the virtual environment on Linux (bash)


#. In the same command window, use ``pip``, the package installer for Python, to
   install the PyFluent packages::

    python -m pip install ansys-fluent-core   # Access Fluent’s core capabilities (mesh, solve, postprocess)
    python -m pip install ansys-fluent-parametric   # Access Fluent’s parametric capabilities (optional)
    python -m pip install ansys-fluent-visualization   # Access Fluents postprocessing capabilities, which work with PyVista and Matplotlib (optional)


Which version of Python should you use?
---------------------------------------
PyFluent supports Python 3.7 through Python 3.10 on Windows and Linux. Python 3.7 is shipped
with Ansys 2022 R2 and later. For example, in a 2022 R2 installation, the executable file for
installing Python 3.7 is likely in
``C:\Program Files\ANSYS Inc\v222\commonfiles\CPython\3_7\winx64\Release\python.exe``.

Alternatively, you can download any compatible version of Python directly from the
`Downloads page <https://www.python.org/downloads/>`_ of the Python web site.

In either case, run the Python executable file as an administrator, selecting the
**Add Python 3.9 to PATH** checkbox on the first wizard page before proceeding with
the installation. On the last wizard page, which indicates that Python is installed
successfully, follow the instructions for disabling the path length limit if you have
long file paths.

Where do you find source code and documentation?
------------------------------------------------
All PyAnsys public libraries are available from the `PyAnsys GitHub account <https://github.com/pyansys>`_.
The **Repositories** page displays the number of repositories, which are searchable by name.
For example, to find all PyFluent libraries, type ``pyfluent`` in the search option. 

The ``README.md`` file for the PyAnsys Github account lists the public PyAnsys libraries.
The links in this list are to the documentation for the respective libraries. In addition to 
general usage information, the documentation for a library includes many practical examples.

How do you launch Fluent using PyFluent?
----------------------------------------
To launch Fluent with PyFluent commands, use this code:

.. code:: python

   import ansys.fluent.core as pyfluent
   session=pyfluent.launch_fluent()


This example shows you how to launch a double precision Fluent session with two
processars and the Fluent GUI:

.. code:: python

   session=pyfluent.launch_fluent(precision="double", processor_count=2, show_gui=True)


For additional launch examples, see :ref:`ref_user_guide_launch`. For descriptions of all parameters,
see the :func:`launch_fluent() <ansys.fluent.core.launcher.launcher.launch_fluent>` method.

How do you learn how to use PyFluent?
-------------------------------------
Depending on how you prefer to learn, you can use any or all of these methods
to learn how to use PyFluent:

- Review the examples in the documentation, working first through those provided in
  the :ref:_ref_example_gallery in this guide and then through those provided in the
  **Examples** sections in the `PyFluent-Parametric <https://fluentparametric.docs.pyansys.com/>`_ and
  `Pyfluent-Visusalization <https://fluentvisualization.docs.pyansys.com/>`_
  guides.
- Record a journal of your actions in Fluent and review the corresponding script.
  
  .. note::
     In Fluent 2022 R2, recording a journal of your Fluent meshing commands does not
     produce a Python script that is in PyFluent syntax. However, there is a
     one-to-one correspondence between the recorded Python command and the equivalent
     PyFluent command. This means that you can manually translate the recorded Python
     command to the PyFluent syntax.

  
  Here is a Python command recorded in Fluent:

  .. code:: python

    import :(%py-exec "workflow.TaskObject['Describe Geometry and Flow'].Arguments.setState({r'AddEnclosure': r'No',r'CloseCaps': r'Yes',r'FlowType': r'Internal flow through the object',})")


  Here is the manually translated equivalent command in PyFluent syntax:
  
  .. code:: python

    session.meshing.workflow.TaskObject['Describe Geometry and Flow'].Arguments.setState(({r'AddEnclosure': r'No',r'CloseCaps': r'Yes',r'FlowType': r'Internal flow through the object’,})


- Write scripts, using capabilities such as these:

  - IntelliSense to show available options for any given command. For example,
    in `JupyterLab <https://jupyter.org/>`_, press the tab key.
  - Standard Python or PyAnsys tooling to print options related to a specified
    object. For example, use ``dir (<object>)`` or ``help (<object>)``.

How do you get help for PyFluent?
---------------------------------
Because PyFluent libraries are open source, support for issues, bugs, and feature
requests are available in their respective GitHub repositories.

- To log an issue for PyFluent, use the `PyFluent Issues page <https://github.com/pyansys/pyfluent/issues>`_.
- To start a discussion, use the `PyFluent Discussions page <https://github.com/pyansys/pyfluent/discussions>`_.

For discussions about developer tools, engineering simulation, and physics for Ansys software,
visit the `Ansys Developer portal <https://developer.ansys.com/>`_. The
`Ansys Discuss <https://discuss.ansys.com/>`_ page is where users, partners, students, and
Ansys subject matter experts connect, share ideas, discuss the latest technologies, and ask
questions to quickly obtain help and guidance. On this page, you can filter discussions by
category or apply the **Fluent** tag to view only Fluent-related discussions.
