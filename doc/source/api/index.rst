.. _ref_api:

API reference
=============

This is PyFluent's class and function reference. Please refer to the :ref:`ref_user_guide` for
full guidelines on their use.

All the public APIs for PyFluent are listed in the left hand margin. Some key APIs are mentioned below:
 
Meshing mode
---------------
 
The following interfaces are specific to meshing mode.

* :ref:`meshing <ref_meshing_datamodel_meshing>`
* :ref:`PartManagement <ref_meshing_datamodel_PartManagement>`
* :ref:`PMFileManagement <ref_meshing_datamodel_PMFileManagement>`
* :ref:`workflow <ref_meshing_datamodel_workflow>`
* :ref:`meshing utilities <ref_meshing_datamodel_MeshingUtilities>`

Solution mode
-------------
 
The solver :ref:`settings API <ref_root>` is the main interface for controlling and running the solver.


.. toctree::
    :maxdepth: 2
    :hidden:
    :caption: ansys.fluent.core

    filereader/index
    launcher/index
    meshing/index
    post_objects/index
    scheduler/index
    services/index
    solver/index
    streaming_services/index
    utils/index
    data_model_cache
    exceptions
    file_session
    fluent_connection
    journaling
    logging
    parametric
    rpvars
    search
    session_base_meshing
    session_meshing
    session_pure_meshing
    session_solver_icing
    session_solver_lite
    session_solver
    session
    systemcoupling
    warnings
    workflow
