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

  >>> from ansys.fluent.core import Meshing
  >>> meshing_session = Meshing.from_install()

  >>> # Feature is available before enabling beta features, but unusable and raises 'BetaFeaturesNotEnabled'
  >>> assert hasattr(meshing_session, "topology_based")
  >>> assert "topology_based" in dir(meshing_session)

  >>> topo_meshing = meshing_session.topology_based()
  ansys.fluent.core.diagnostics.exceptions.BetaFeaturesNotEnabled: The feature 'topology_based' requires 'enable_beta_features' flag to be enabled.

  >>> # Enable beta features
  >>> meshing_session.enable_beta_features()

  >>> # Feature is now usable
  >>> topo_meshing = meshing_session.topology_based()
  >>> topo_meshing
  <ansys.fluent.core.meshing.meshing_workflow.TopologyBasedMeshingWorkflow object at 0x0000024D574410F0>


Solver Session
--------------

.. note::

   The ability to **switch to meshing mode** (via ``switch_to_meshing()``) is now a stable feature. It is available in Ansys Fluent 2025 R2 and later.

For information on using the ``switch_to_meshing()`` method, see the :ref:`ref_switching_between_solver_and_meshing_sessions` section in the session documentation.


.. note::

   Beta features are actively developed and may evolve over time. They are provided to allow early
   access to upcoming capabilities in Fluent and may undergo changes in behavior or interface in future
   releases. They may not yet be fully supported in all workflows. Feedback from users is encouraged
   and helps guide ongoing development.
