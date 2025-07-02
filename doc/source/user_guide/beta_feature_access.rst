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

The **Topology-Based Meshing** workflow is available as a beta feature in meshing mode.

To enable and access it:

.. code-block:: python

  >>> import ansys.fluent.core as pyfluent
  >>> meshing_session = pyfluent.launch_fluent(mode="meshing")

  >>> # Feature is available before enabling beta features, but unusable and raises 'BetaFeaturesNotEnabled'
  >>> assert hasattr(meshing_session, "topology_based")
  >>> assert "topology_based" in dir(meshing_session)

  >>> topo_meshing = meshing_session.topology_based()
  ansys.fluent.core.exceptions.BetaFeaturesNotEnabled: The feature 'topology_based' requires 'enable_beta_features' flag to be enabled.

  >>> # Enable beta features
  >>> meshing_session.enable_beta_features()

  >>> # Feature is now usable
  >>> topo_meshing = meshing_session.topology_based()
  >>> topo_meshing
  <ansys.fluent.core.meshing.meshing_workflow.TopologyBasedMeshingWorkflow object at 0x0000024D574410F0>


Solver Session
--------------

The ability to **switch to meshing mode** from a solver session is a beta feature.

To enable and use it:

.. code-block:: python

  >>> solver_session = pyfluent.launch_fluent()

  >>> # Method available before enabling beta features, but unusable and raises 'BetaFeaturesNotEnabled'
  >>> assert hasattr(solver_session, "switch_to_meshing")

  >>> switched_meshing_session = solver_session.switch_to_meshing()
  ansys.fluent.core.exceptions.BetaFeaturesNotEnabled: The feature 'switch_to_meshing' requires 'enable_beta_features' flag to be enabled.

  >>> # Enable beta features
  >>> solver_session.enable_beta_features()

  >>> # Method is now usable
  >>> switched_meshing_session = solver_session.switch_to_meshing()
  >>> assert switched_meshing_session.is_active()
  >>> assert not solver_session.is_active()


.. note::

   Beta features are subject to change and may not be fully supported in all versions of Fluent.
   Use them with caution in production workflows. Feedback on beta features is encouraged and
   helps improve future releases.