.. _ref_user_guide_tui_commands:

Using TUI commands
==================

TUI commands refer to a programming interface that mirrors the Fluent TUI (text user
interface). There is a TUI command hierarchy defined for each mode, meshing and solution.
The hierarchy that is active depends on the current Fluent mode. The guidance here applies
to either mode.

The PyFluent TUI commands allow you to automate workflows comprehensively. Everything
that's in the Fluent TUI (which itself is a comprehensive automation interface)
is exposed in PyFluent. The PyFluent TUI commands are Pythonic versions of those used
in the Fluent console.

The PyFluent TUI commands do not support TUI features such as aliases or
command abbreviation. To make using PyFluent commands in an interactive
session easier, you can install a tool such as
`pyreadline3 <https://github.com/pyreadline3/pyreadline3>`_, which provides
both command line completion and history. To inspect any PyFluent TUI object further,
you can also use the Python built-in functions,
`help <https://docs.python.org/3/library/functions.html#help>`_ and 
`dir <https://docs.python.org/3/library/functions.html#dir>`_.

The arguments to a TUI command are just those that would be passed in direct interaction with the
Fluent Console, but in a Pythonic style. Because the most productive way to write Python commands
is with reference to existing TUI commands, look at how the Python usage mirrors existing TUI usage.

Assume in the solution mode, you typed the following in the Fluent console to set
velocity inlet properties:

.. code:: lisp

    /define/boundary_conditions/set/velocity-inlet

This command instigates a sequence of prompts for input in the console. Assume that you respond
to each prompt in turn as follows:

.. code:: lisp

    velocity-inlet-5 
    
    () 
    
    temperature 
    
    no 
    
    293.15 
    
    quit

The effect is identical to the following code that specifies all the arguments in one call:

.. code:: lisp

    /define/boundary-conditions/set/velocity-inlet velocity-inlet-5 () temperature no 293.15 quit

Interactive TUI usage then is a reliable approach for constructing full TUI calls, including full sequences of
arguments. With the full TUI call in hand, the next step is to transform it to a Python call:

.. code:: python

    from ansys.fluent.core import launch_fluent

    solver_session = launch_fluent()

    tui = solver_session.solver.tui

    tui.define.boundary_conditions.set.velocity_inlet(
      "velocity-inlet-5", [], "temperature", "no", 293.15, "quit"
      )

Now look at another Fluent console interaction:

.. code:: lisp

    /define/units

    pressure

    "Pa"

The Python call is:

.. code:: python

    tui.define.units("pressure", '"Pa"')

The string "Pa" is wrapped in single quotes to preserve the double quotes around the TUI argument.

Note the following rules implied in the preceding examples:

- Each forward slash separator between elements in TUI paths is transformed to Python dot notation.
- Some characters in path elements are either removed or replaced because they are illegal inside Python names.
  For example:
  
  - Each hyphen in a path element is transformed to an underscore.
  - Each question mark in a path element is removed.

- Some are some rules about strings:
  
  - String-type arguments must be surrounded by quotation marks in Python.
  - Note the special case in the last Python call example where a target Fluent TUI argument was surrounded
    by quotation marks (`"Pa"`). To preserve  quotations, you must wrap Python string in additional single
    quotation marks.
  - The contents of string arguments are preserved.

For more examples of TUI command usage, see :ref:`ref_mixing_elbow_tui_api`.
