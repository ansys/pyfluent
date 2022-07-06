.. _ref_index_api:

=============
API Reference
=============

This section describes the core pythonic interfaces for Fluent. 
Here, you can find the application programming interfaces for 
such things as launching Fluent, assorted utilities, as well as 
the APIs for the meshing and solver components of Fluent. 

ANote that aside from the core API, there is also the separate 
Parametric Study API, as well as the separate Visualization API.

Launching Fluent
----------------

The API for this component provides access to starting Fluent locally in 
server mode or connecting to a running Fluent server instance.

Pythonic Utilities
------------------

The API is currently comprosed of only a function to allow for 
asynchonous execution.

Meshing Mode
------------

The meshing API is dedicated to capturing the capabilities of 
the Fluent Meshing guided workflows and associated tools. The API 
consists of a TUI-based API that is derived from the Fluent (meshing) 
text command interface, as well as a datamodel-driven meshing workflow 
interface that manages the workflow tasks, meshing functions, and 
part management.

Solver Mode
-----------

The solver API is dedicated to capturing the power of the 
Fluent solver. The API consists of a settings-based API (beta) 
or TUI-based API that is derived from the Fluent (solver) text 
command interface, as well as access to Fluent surface, scalar 
and vector field data. 

.. currentmodule:: ansys.fluent

.. autosummary::
   :toctree: _autosummary

.. toctree::
   :maxdepth: 4
   :hidden:
   
   core/index