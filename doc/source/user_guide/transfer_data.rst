.. _ref_data_transfer_guide:

Transferring session data
=========================

Use :func:`transfer_case() <ansys.fluent.core.connectivity.data_transfer.transfer_case>` to transfer a case or mesh
from a source session (meshing or solver) to one or more destination solver sessions.

Meshing to solver
-----------------

.. code:: python

  >>> import ansys.fluent.core as pyfluent
  >>> from ansys.fluent.core.examples import download_file
  >>> from ansys.fluent.core.connectivity.data_transfer import transfer_case

  >>> mesh_file_name = download_file("mixing_elbow.msh.h5", "pyfluent/mixing_elbow")

  >>> source = pyfluent.PureMeshing.from_install()
  >>> source.meshing_workflow.application.file.read_mesh(file_name=mesh_file_name)

  >>> solver = pyfluent.Solver.from_install()
  >>> transfer_case(source_instance=source, solvers=[solver], file_type="mesh")

Solver to solver
----------------

``file_type`` defaults to ``"case"``, so you can omit it here.

.. code:: python

  >>> import ansys.fluent.core as pyfluent
  >>> from ansys.fluent.core.examples import download_file
  >>> from ansys.fluent.core.connectivity.data_transfer import transfer_case

  >>> case_file_name = download_file("mixing_elbow.cas.h5", "pyfluent/mixing_elbow")

  >>> source = pyfluent.Solver.from_install()
  >>> source.settings.file.read_case(file_name=case_file_name)

  >>> target = pyfluent.Solver.from_install()
  >>> transfer_case(source_instance=source, solvers=[target])
