.. _faqs:
Frequently asked questions
==========================

What is PyAnsys?
----------------
PyAnsys is a set of open source technologies that allow you to interface with Ansys Fluent,
MAPDL, AEDT, and other Ansys products Pythonically. You can use PyAnsys libraries within
a Python environment of your choice in conjunction with external Python libraries.

# .. image:: /_static/PyAnsys_overview.png
#   :width: 500pt
#   :align: center


What is PyFluent?
-----------------
PyFluent provides Pythonic access to Ansys Fluent. Its features enable the seamless use of Fluent
within the Python ecosystem and broad access to native Fluent features, including the ability to
perform these actions:

- Launch Fluent using a local Ansys installation.
- Use Fluent's TUI (text user interface) commands for both meshing and solver features.
- Use Fluent's built-in postprocessing capabilities.

PyFluent is not bundled with the Fluent installation. It must be downloaded and installed separately as
indicated in :ref:`installation`.

PyFluent has no graphical user interface. You interact with it through the Python environment of your choice.

How does PyFluent compare to UDFs?
----------------------------------
PyFluent is conceptually aligned with the TUI console commands (and journaling) rather than with
UDFs (user-defined functions). In other words, PyFluent is used for automation rather than
modifying the solver behavior.

UDFs continue to be written in C and remain important elements of
Fluent simulations.

While you cannot write UDFs in Python, you can execute PyFluent commands to compile and load UDFs,
similar to how you use TUI commands for doing so.

Who should use PyFluent?
------------------------
This image shows the many types of people who are using PyFluent and how it benefits
them:

# .. image:: /_static/who_why_use_PyFluent.png
#   :width: 500pt
#   :align: center


Using PyFluent allows you to acheive these objectives:

- Enhance productivity with customized scripts.
- Automate workflows customized scripts.
- Extend CFD simulations to a wider audience.
- Create comprehensive workflows inspired by Python's increasingly broad appeal
  in these areas of scientific computing:

  - Computer vision
  - Artificial intelligence (AI)
  - Machine learning (ML)
  - Data processing and visualization
  - Optimization

- Benefit from widely accepted libraries and notation for computing with
  multi-dimensional arrays in the Python environment.

# .. image:: /_static/libraries_notations.png
#   :width: 500pt
#   :align: center


What can you do with PyFluent?
------------------------------
PyFluent allows you to do many things, including:

- Seamlessly integegrate Fluent as a solver into your in-house design tools.
- Customize postprocessing, perhaps by using Python's vast external
  library to extend postprocessing capabilities or by automatically generating
  a PowerPoint presentation for simulation results.
- Use a web app to access jobs running on a cluster, monitor convergence, and
  generate graphs.
- Leverage ML and AI, especially for models that are solved quickly but can be
  improved as additional knowledge is acquired and applied.
- Use Python APIs to couple together different Ansys products.

.. _faq_install_venv:
How do you install PyFluent?
----------------------------
Before you install PyFluent, you must install Python. For version information,
see the next question. In addition to the procedural information that follows,
see :ref:`installation`.

#. Install Fluent 2022 R2 or later.
#. Set the environment variable for this Ansys release to point to the installation
   folder.
   
   For example, for 2022 R2, you might set ``AWP_ROOT222`` to point to
   ``C:\Program Files\ANSYS Inc\v222``.

   While you must explicitly set this on Linux, it should be automatically set
   on Windows.

#. In a command window, create a local Python *virtual environment* installation
   with this code:

   .. code:: python
      python -m venv pyenv		# Setup a local virtual environment
      pyenv\Scripts\activate	# Activate the virtual environment Windows
      source pyenv/bin/activate.csh	# Activate the virtual environment Linux (csh)
      . pyenv/bin/activate		# Activate the virtual environment Linux (bash)


#. In the same command window, use pip to install the Fluent Python packages:

   .. code:: python
      python -m pip install ansys-fluent-core		# Access Fluent’s core capabilities (mesh, solve, postprocessing)
      python -m pip install ansys-fluent-parametric	# Access Fluent’s parametric capabilities (optional)
      python -m pip install ansys-fluent-visualization	# postprocessing capability that works with PyVista and Matplotlib (optional)

Which version of Python should you use?
---------------------------------------
PyFluent can be used with Python 3.7 and later. Python 3.7 is shipped with
the Ansys 2022 R2 release. The executable file is located in
``C:\Program Files\ANSYS Inc\v222\commonfiles\CPython\3_7\winx64\Release\python.exe``.

Alternatively, you can download any compatible version directly from the `Downloads page <https://www.python.org/downloads/`_
of the Python web site.

Run the executable file as an administrator, selecting the **Add Pyhthon 3.9 to PATH** checkbox
on the first wizard page before proceeding with the installation. After Python is installed
successfully, if you have long file paths, follow the instructions on the last wizard page for
disabling the path length limit to prevent future issues.
