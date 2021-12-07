PyFluent
========
Fluent's SolverAPI exposed in Python

Installation
------------
For a local "development" version, install with:

.. code:: console

  git clone https://github.com/pyansys/pyfluent.git
  cd pyfluent
  pip install grpc\ansys-api-fluent-v0-0.0.1.tar.gz
  pip install -e .

We need to install the grpc package as it is not yet in PyPI.

Usage
-----
1) Run Fluent from the latest develop branch.
2) In the Fluent Console (TUI) execute the following Scheme code: (enable-feature 'new-tui)
3) Start the server with server.txt as server-info filename. 
   E.g., from the Fluent UI File Menu, select Applications > Server > Start ... . Enter server.txt in the dialog and select OK.

In Python (client-side):

.. code:: python

  import ansys.fluent.solver as pyfluent
  pyfluent.start(r'<path-to-server-file>/server.txt')
  pyfluent.file.read_case(case_file_name='tet.cas.gz')
  #etc.
  pyfluent.stop()

