.. _ref_index_api:

=============
API reference
=============

This page details the public modules, functions, classes and methods
provided by PyFluent, describing what they are and what they do. To
learn how to use PyFluent, see the :ref:`ref_user_guide`.

As explained in the :ref:`ref_user_guide`, each Fluent server mode
provides a specific set of API objects. You can access those API
objects by first calling ``launch_fluent``.

Launching Fluent
----------------

A ``launch_fluent`` function is provided to start and connect to Fluent
locally or connect to a running Fluent, either locally or remote.

Meshing mode
------------

In Fluent meshing mode, the API consists of:
* a ``tui`` object to provide Pythonic object-based access to all of
  Fluent's TUI (text user interface) commands in meshing mode, precisely 
  following the TUI format
* a ``meshing`` and a ``workflow`` object, which together provide access 
  to Fluent's meshing workflow feature. The same objects have been in 
  Fluent meshing's Python console over several releases
* a PartManagement and a PMFileManagement object, which together
  provide access to Fluent meshing's part management capability, Again
  these objects have been in the Python console for some time
* a preferences object for managing Fluent user preferences

Solver mode
-----------

In Fluent meshing mode, the API consists of:
* a ``tui`` object to provide Pythonic object-based access to all of
  Fluent's TUI (text user interface) commands in solver mode,
  precisely following the TUI format
* a ``solver`` object providing access to :ref:`ref_settings` providing 
  a natural way to access and modify Fluent solver
  settings and issue commands following a new format
* a preferences object for managing Fluent user preferences


.. currentmodule:: ansys.fluent

.. autosummary::
   :toctree: _autosummary

.. toctree::
   :maxdepth: 4
   :hidden:
   
   launcher
   meshing/index
   solver/index
   utils
   filereader



