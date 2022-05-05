.. _ref_solver_tui:

Solver TUI
==========
The PyFluent solver text user interface (TUI) API is provided to command the
Fluent solver using commands that are Pythonic versions of the TUI commands used
in the Fluent console.  Much like Fluent's TUI the API provides a hierarchical
interface to the underlying procedural interface of the program.

The solver TUI API does not support Fluent TUI features such as aliases or
command abbreviation.  As an alternative, using this API in an interactive
session is easier if you install a tool such as
`pyreadline3 <https://github.com/pyreadline3/pyreadline3>`_ which provides
both command line completion and history.  You can also use Python standard
`help` and `dir` commands on any object in the API to inspect it further.

The TUI based examples in our gallery provide a guide for how to use this API.

.. currentmodule:: ansys.fluent.core.solver

.. autosummary::
   :toctree: _autosummary

.. autoclass:: ansys.fluent.core.solver.tui::main_menu.adjoint
.. autoclass:: ansys.fluent.core.solver.tui::main_menu.display
.. autoclass:: ansys.fluent.core.solver.tui::main_menu.define
.. autoclass:: ansys.fluent.core.solver.tui::main_menu.file
.. autoclass:: ansys.fluent.core.solver.tui::main_menu.icing
.. autoclass:: ansys.fluent.core.solver.tui::main_menu.mesh
.. autoclass:: ansys.fluent.core.solver.tui::main_menu.parameters__and__customization
.. autoclass:: ansys.fluent.core.solver.tui::main_menu.parallel
.. autoclass:: ansys.fluent.core.solver.tui::main_menu.plot
.. autoclass:: ansys.fluent.core.solver.tui::main_menu.preferences
.. autoclass:: ansys.fluent.core.solver.tui::main_menu.report
.. autoclass:: ansys.fluent.core.solver.tui::main_menu.results
.. autoclass:: ansys.fluent.core.solver.tui::main_menu.solution
.. autoclass:: ansys.fluent.core.solver.tui::main_menu.solve
.. autoclass:: ansys.fluent.core.solver.tui::main_menu.setup
.. autoclass:: ansys.fluent.core.solver.tui::main_menu.surface
.. autoclass:: ansys.fluent.core.solver.tui::main_menu.server
.. autoclass:: ansys.fluent.core.solver.tui::main_menu.turbo_post
.. autoclass:: ansys.fluent.core.solver.tui::main_menu.views
.. autoclass:: ansys.fluent.core.solver.tui::main_menu.parametric_study
.. autoclass:: ansys.fluent.core.solver.tui::main_menu.turbo_workflow
