.. _ref_user_guide_tui_api:

Using the TUI APIs
==================

TUI API refers to a programming interface that mirrors the Fluent text user
interface (TUI). There is a TUI API defined for each of meshing and solution mode -
which API is active depends on the current Fluent mode. The guidance here is 
applicable to either mode.

The TUI APIs represent a means to automate workflows comprehensively: everything
that's in the Fluent TUI (which itself is a comprehensive automation interface)
is in the TUI API. The TUI APIs provide commands that are Pythonic versions of the TUI commands used
in the Fluent console. Much like Fluent's TUI the API provides a hierarchical
interface to the underlying procedural interface of the program.

The TUI APIs do not support Fluent TUI features such as aliases or
command abbreviation. As an alternative, using these APIs in an interactive
session is easier if you install a tool such as
`pyreadline3 <https://github.com/pyreadline3/pyreadline3>`_ which provides
both command line completion and history. You can also use Python built-in functions,
`help <https://docs.python.org/3/library/functions.html#help>`_ and 
`dir <https://docs.python.org/3/library/functions.html#dir>`_ on any object in the API to inspect it further.

The arguments to a TUI command are just those that would be passed in direct interaction with the
Fluent Console, but in a Pythonic style. Let's look in more detail at how the API usage mirrors 
existing TUI usage, because the most productive way to write TUI API Python commands is with reference to
existing TUI commands. For instance, in solution mode:

.. code:: lisp

    /define/boundary_conditions/set/velocity-inlet

can be typed into the Fluent console in solution mode in order to set
velocity inlet properties. The above call instigates a sequence of prompts 
for input in the console, such that if the user responds to each prompt in turn:

.. code:: lisp

    velocity-inlet-5 
    
    () 
    
    temperature 
    
    no 
    
    293.15 
    
    quit

the effect will be identical to the following statement that specifies all the arguments in the call:

.. code:: lisp

    /define/boundary-conditions/set/velocity-inlet velocity-inlet-5 () temperature no 293.15 quit

Interactive TUI usage then is a reliable approach for constructing full TUI calls including full sequences of
arguments. With the full TUI call in hand, the next step is to transform it to a Python call:

.. code:: python

    from ansys.fluent.core import launch_fluent

    solver_session = launch_fluent()

    tui = solver_session.solver.tui

    tui.define.boundary_conditions.set.velocity_inlet(
      "velocity-inlet-5", [], "temperature", "no", 293.15, "quit"
      )

Now look at another console interaction to illustrate a specific point:

.. code:: lisp

    /define/units

    pressure

    "Pa"

The Python analogue is:

.. code:: python

    tui.define.units("pressure", '"Pa"')

where the string "Pa" is wrapped in single quotes in order to preserve the double quotes around the TUI argument.

Note the following rules implied in the above examples:

- Each forward slash separator between elements in TUI paths is transformed to Python dot notation
- Some characters in path elements are either removed or replaced because they are illegal inside Python names:
  
  - Each hyphen in a path element is transformed to an underscore
  - Each question mark in a path element is removed

- Some rules about strings:
  
  - Of course, string-type arguments have to be quoted in Python
  - Note the special case where a target Fluent TUI argument needs to be quoted (e.g. "Pa" above). 
    That quoting has to be preserved by wrapping the Python string in additional single quotes
  - The contents of string arguments are preserved

There are plenty of additional examples of TUI API usage in :ref:`ref_mixing_elbow_tui_api`.
