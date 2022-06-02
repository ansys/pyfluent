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

The TUI based examples in our gallery provide a guide for how to use this API.
"""
}
