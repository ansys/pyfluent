MENU_DESCRIPTIONS = {
    "solver.tui": """The PyFluent solver text user interface (TUI) API is provided to command the
Fluent solver using commands that are Pythonic versions of the TUI commands used
in the Fluent console.  Much like Fluent's TUI the API provides a hierarchical
interface to the underlying procedural interface of the program.

The solver TUI API does not support Fluent TUI features such as aliases or
command abbreviation.  As an alternative, using this API in an interactive
session is easier if you install a tool such as
`pyreadline3 <https://github.com/pyreadline3/pyreadline3>`_ which provides
both command line completion and history.  You can also use Python standard
`help` and `dir` commands on any object in the API to inspect it further.

The arguments to a TUI command are just those that would be passed in direct interaction with the
Fluent Console, but in a Pythonic style. For instance the TUI command /define/models/energy? #t becomes
_session_.solver.tui.define.energy(False).

Care must be taken wherever the TUI expects a quoted string as input: in such cases the Python argument
should be provided as a double quoted string embedded inside single quotes. For instance
/define/boundary_conditions/velocity_inlet "IF(t<=10e-6[sec],3.58[m/s]*cos(PI*t/30e-6[s]),0[m/s])"
in the TUI would be written as session.solver.tui.define.boundary_conditions.velocity_inlet("inlet2", "no", "no", "yes", "yes", "no",
'"IF(t<=10e-6[sec],3.58[m/s]*cos(PI*t/30e-6[s]),0[m/s])"', "no", 0, "no", 300, "no", "no", "no", "yes", 10, 0.04) in Python.

The TUI based examples in our gallery provide a guide for how to use this API.
"""
}
