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
 1) Run Fluent from latest development branch with PyFluent preparation changes.
 2) Execute in Fluent TUI: (enable-feature 'new-tui)
 3) Start the server with server.txt as server-info filename

 In Python (client-side):

.. code:: python

  from ansys.fluent.solver import fluent_pymenu as fluent
  fluent.start(r'c:\Users\mkundu\ANSYSDev\work\server.txt')
  fluent.file.read_case(case_file_name='tet.cas.gz')
  etc.
  fluent.stop()

