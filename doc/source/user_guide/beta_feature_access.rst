.. _ref_beta_feature_access:

Beta features
=============

PyFluent provides access to experimental or under-development capabilities of
Fluent via **beta features**. These features are disabled by default and can be
enabled at runtime by calling the `enable_beta_features()` method on a session object.
Once activated, the additional beta methods and workflows become available.

Currently, limited beta features are available in both **Meshing** and **Solver** sessions.

Meshing Session
---------------

The **Topology-Based Meshing** workflow is available as a beta feature in the meshing mode.

To enable and access it:

.. code-block:: python

  >>> import ansys.fluent.core as pyfluent
  >>> meshing_session = pyfluent.launch_fluent(mode="meshing")

  >>> # Feature is unavailable before enabling beta features
  >>> "topology_based" in dir(meshing_session)
  False

  >>> # Enable beta features
  >>> meshing_session.enable_beta_features()

  >>> # Feature is now accessible
  >>> "topology_based" in dir(meshing_session)
  True

  >>> topo_meshing = meshing_session.topology_based()
  >>> topo_meshing
  <ansys.fluent.core.meshing.meshing_workflow.TopologyBasedMeshingWorkflow object at 0x0000024D574410F0>


Solver Session
--------------

The ability to **switch to meshing mode** from a solver session is a beta feature.

To enable and use it:

.. code-block:: python

  >>> solver_session = pyfluent.launch_fluent()

  >>> # Method unavailable before enabling beta
  >>> "switch_to_meshing" in dir(solver_session)
  False

  >>> # Enable beta features
  >>> solver_session.enable_beta_features()

  >>> # Method is now available
  >>> "switch_to_meshing" in dir(solver_session)
  True

  >>> switched_meshing_session = solver_session.switch_to_meshing()
  >>> switched_meshing_session.is_active()
  True
  >>> solver_session.is_active()
  False


.. note::

   Beta features are subject to change and may not be fully supported in all versions of Fluent.
   Use them with caution in production workflows. Feedback on beta features is encouraged and
   helps improve future releases.