.. _ref_beta_feature_access:

Beta features
=============

PyFluent provides access to experimental Fluent capabilities through **beta features**. These features
are intended for early access, evaluation, and feedback, and may be subject to change in future releases.

Beta features are not enabled by default. To access them, call the ``enable_beta_features()`` method
on a session object. After doing so, additional methods specific to that session type become usable.

Beta features differ between **Meshing** and **Solver** sessions. Each session exposes a distinct
set of beta-specific capabilities that are only operable after the beta mode is explicitly enabled.

Meshing Session
---------------

In meshing mode, the **Topology-Based Meshing** workflow is available as a beta feature. While
the associated method is visible on the session object, attempting to use it without enabling beta
features results in a ``BetaFeaturesNotEnabled`` exception.

Example usage:

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

In solver mode, the ability to **switch to meshing mode** is available as a beta feature.
Similar to the meshing session, the method is present on the session object but raises
``BetaFeaturesNotEnabled`` until beta features are enabled.

Example usage:

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

   Beta features are actively developed and may evolve over time. They are provided to allow early
   access to upcoming capabilities in Fluent and may undergo changes in behavior or interface in future
   releases. They may not yet be fully supported in all workflows. Feedback from users is encouraged
   and helps guide ongoing development.
