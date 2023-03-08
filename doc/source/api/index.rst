API reference
=============

This section describes the core Pythonic interfaces for Fluent. Here, you can find the application programming
interfaces for such things as launching Fluent, assorted utilities, as well as the interfaces for the meshing and
solver components of Fluent.

General
#######

The :ref:`ref_general` component describes starting of Fluent and it's asynchronous execution, types of various
Fluent sessions, use of gRPC and streaming services, creation of visualization objects for Matplotlib and abstract
machine object for queue system interface, contains examples to read and transfer Fluent's case files in addition
to this it contains information about used meta classes, rpvars, workflow objects, recording journals and module for
creation of  physical quantities using real values and units.

Meshing
#######

The :ref:`ref_meshing` mode is dedicated to capturing the capabilities of the Fluent Meshing guided workflows and
associated tools. This component consists of an interface that is derived from the Fluent (meshing) TUI, as well as
a meshing workflow interface that manages workflow tasks, meshing functions, and part management.

Solver
######

The :ref:`ref_solver` mode is dedicated to capturing the power of the Fluent solver. This component consists of a
:ref:`ref_settings`-based interface or a :ref:`ref_solver_tui`-based interface that is derived from the Fluent
(solver) TUI, as well as access to Fluent surface, scalar and vector field data.


.. toctree::
    :maxdepth: 2
    :hidden:

    general/index
    meshing/index
    solver/index
