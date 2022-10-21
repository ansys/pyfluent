.. _ref_casereader:

Case reader
===========

Case reader provides a reader for fluent case files.

Sample usage
------------

You can use the case reader by importing it and passing a case file path.
The following example show the usage of case reader with a case file (.cas.h5)
read from examples repository as shown:

.. code-block:: python

  >>> from ansys.fluent.core import examples
  >>> from ansys.fluent.core.filereader.casereader import CaseReader

  >>> case_filepath = examples.download_file("Static_Mixer_Parameters.cas.h5", "pyfluent/static_mixer")
  >>> reader = CaseReader(case_filepath=case_filepath)
  >>> reader.precision()
  2
  >>> reader.num_dimensions()
  3
  >>> {p.name: p.value for p in reader.input_parameters()}
  {'inlet1_vel': '1 [m/s]', 'inlet1_temp': '300 [K]', 'inlet2_vel': '1 [m/s]', 'inlet2_temp': '350 [K]'}
  >>> {p.name: p.units for p in reader.output_parameters()}
  {'outlet-temp-avg-op': 'K', 'outlet-vel-avg-op': 'm s^-1'}

Additional features
-------------------
Along with the basic functionality, case reader also has a bunch of useful features, like:

Supports multiple file formats
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The case reader can read fluent case files in .cas, .cas.h5 and .cas.gz in both text and binary formats.

Takes project path as argument
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Case reader also has an option to take a fluent project path (.flprj) as argument and locate the
case file path.

.. code-block:: python

  >>> reader = CaseReader(project_filepath="Dir1/Dir2/project.flprj")

Capability to read 'rp' and 'config' vars
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Case reader can provide the 'rp' and 'config' vars as well.

.. code-block:: python

  >>> reader.rp_vars()
  >>> reader.config_vars()
