.. _ref_general:

General
=======

Launcher
########

:ref:`ref_launcher` provides access to starting Fluent locally in server mode or connecting to a running Fluent
server instance.

Asynchronous execution
######################

:ref:`ref_utils` consists solely of a function to allow for asynchronous execution.

Sessions
########

:ref:`ref_sessions` consists of available Fluent sessions.

Services
########

:ref:`ref_services` consists of gRPC services for Fluent sessions.

Streaming services
##################

:ref:`ref_streaming_services` consists of streaming services for management of gRPC services.

Post objects
############

:ref:`ref_post_objects` consists of visualization objects for Matplotlib.

Scheduler
#########

:ref:`ref_scheduler` consists of abstract machine objects and their use for queue system interface.

Case reader
###########

:ref:`ref_case_reader` demonstrates reading of Fluent's case files.

Data transfer
#############

:ref:`ref_data_transfer` demonstrates transfer of Fluent's case files.

Journaling
##########

:ref:`ref_journaling` consists of read-write of journal.

Meta
####

:ref:`ref_meta` consists of used meta classes.

Quantity
########

:ref:`ref_quantity` is a module for creation and manipulation of physical quantities.

rpvars
######

:ref:`ref_rpvars` shows access and modification of rpvars.

Workflow
########

:ref:`ref_workflow` used for creation of TaskObject instance.

.. currentmodule:: ansys.fluent.core

.. autosummary::
    :toctree: _autosummary

.. toctree::
    :maxdepth: 2
    :hidden:

    launcher/index
    utils/index
    sessions/index
    services/index
    streaming_services/index
    post_objects/index
    scheduler/index
    case_reader
    data_transfer
    journaling
    meta
    quantity
    rpvars
    workflow
