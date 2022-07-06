.. _ref_index_api:

=============
API Reference
=============

This section describes the core pythonic interfaces for Fluent. 
Here, you can find the application programming interfaces for 
such things as launching Fluent, assorted utilities, as well as 
the interfaces for the meshing and solver components of Fluent. 

Launching Fluent
----------------

This component provides access to starting Fluent locally in 
server mode or connecting to a running Fluent server instance.

Pythonic Utilities
------------------

This component consists solely of a function to allow for 
asynchonous execution.

Meshing Mode
------------

The meshing mode is dedicated to capturing the capabilities of 
the Fluent Meshing guided workflows and associated tools. This component 
consists of an interface that is derived from the Fluent (meshing) 
TUI, as well as a meshing workflow interface that manages workflow 
tasks, meshing functions, and part management.

Solver Mode
-----------

The solver mode is dedicated to capturing the power of the 
Fluent solver. This component consists of a :ref:`ref_settings`-based 
interface or a :ref:`ref_solver_tui`-based interface that is derived 
from the Fluent (solver) TUI, as well as access to Fluent surface, 
scalar and vector field data.

.. currentmodule:: ansys.fluent

.. autosummary::
   :toctree: _autosummary

.. toctree::
   :maxdepth: 4
   :hidden:
   
   core/index