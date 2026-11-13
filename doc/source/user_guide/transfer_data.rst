.. _ref_data_transfer_guide:

.. vale Google.Spacing = NO

Transferring session data
=========================

Use :class:`~ansys.fluent.core.solver.case_snapshot.CaseSnapshot` to copy the
complete setup of a case to one or more solver sessions.
:func:`transfer_case() <ansys.fluent.core.connectivity.data_transfer.transfer_case>`
transfers a case or mesh from a meshing or solver session to solver sessions, as
shown at the end of this page.

Case snapshots
--------------

A ``CaseSnapshot`` holds the complete setup of a case: all its settings and the
mesh they apply to. It is carried by a Fluent case file, Fluent's own complete
record of a case, so it includes settings that the settings API does not expose.
The case file is handled for you, whether Fluent runs locally, in a container, or
remotely through a file transfer service. Solution data is not included.

.. code:: python

  >>> import ansys.fluent.core as pyfluent
  >>> from ansys.fluent.core.examples import download_file

  >>> case_file_name = download_file("mixing_elbow.cas.h5", "pyfluent/mixing_elbow")
  >>> source = pyfluent.Solver.from_install()
  >>> source.settings.file.read_case(file_name=case_file_name)
  >>> source.settings.setup.models.viscous.model = "laminar"

  >>> snapshot = pyfluent.CaseSnapshot.from_session(source)
  >>> workers = [pyfluent.Solver.from_install() for _ in range(2)]
  >>> snapshot.apply_to(*workers)

``from_session`` takes the snapshot immediately: later changes to the source
session are not included, and the snapshot remains usable after that session
exits. ``apply_to`` checks every session first, then loads them in parallel. It
replaces the case of each session, so by default each session also gets the mesh
of the snapshot.

Use ``from_file`` to start from a case file instead of a session, and ``save`` to
keep a copy of a snapshot:

.. code:: python

  >>> template = pyfluent.CaseSnapshot.from_file(case_file_name)
  >>> template.apply_to(source)
  >>> snapshot.save("elbow_laminar.cas.h5")

A snapshot taken from a session is kept in a temporary file, deleted when the
object is garbage-collected. Use a ``with`` block, or call ``close``, to delete it
earlier:

.. code:: python

  >>> with pyfluent.CaseSnapshot.from_session(source) as baseline:
  ...     baseline.apply_to(*workers)

Apply a snapshot without its mesh
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

With ``include_mesh=False``, each session keeps its current mesh and takes only
the settings of the snapshot. Fluent settings apply to zones, so the mesh of the
session must have the same zone names as the snapshot. Otherwise a
``ValueError`` lists the zones that differ, and the session keeps its previous
case. This option uses Fluent's ``mesh.replace`` command.

.. code:: python

  >>> refined = pyfluent.Solver.from_install()
  >>> refined.settings.file.read_case(file_name="elbow_refined.cas.h5")
  >>> snapshot.apply_to(refined, include_mesh=False)

Things to know
~~~~~~~~~~~~~~

* A session must run the Fluent version that wrote the snapshot or a newer one,
  and must have the same dimension. ``apply_to`` checks this before changing any
  session.
* Files that the case refers to, such as compiled UDF libraries and profile
  files, are not copied. Sessions must reach them at the same paths.
* With a file transfer service, each ``apply_to`` uploads a copy of the case to
  the Fluent working directory, where it stays.
* On a session in :ref:`resilient mode <ref_resilient_guide>`, reading the
  snapshot writes an automatic checkpoint first, so
  ``session.resilient.rollback("auto-read_case")`` undoes ``apply_to``. A
  checkpoint named ``case-snapshot`` follows, so that a failover restores the
  applied snapshot.

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
