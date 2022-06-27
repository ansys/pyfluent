.. _ref_user_guide_tui_api:

Using the TUI APIs
==================

TUI API refers to a programming interface that mirrors the Fluent text user
interface (TUI). There is a TUI API defined for each of meshing and solution mode -
which API is active depends on the current Fluent mode.

The TUI APIs represent a means to automate workflows comprehensively: everything
that's in the Fluent TUI (which itself is a comprehensive automation interface)
is in the TUI API.

Let's look at examples of how the API usage mirrors existing TUI usage, because
the most productive way to write TUI API Python commands is with reference to
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

    tui.define.boundary.conditions.set.velocity_inlet(
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
    - Each forward slash (/) separator between elements in TUI paths is transformed to Python dot (.) notation
    - Some characters in path elements are either removed or replaced because they are illegal inside Python names:
      - Each hyphen (-) in a path element is transformed to an underscore (_)
      - Each question mark in a path element is removed
    - Some rules about strings:
      - Of course, string-type arguments have to be quoted in Python
      - Note the special case where a target Fluent TUI argument needs to be quoted - that quoting has to be
        preserved by wrapping the Python string in additional single quotes
      - The contents of string arguments are preserved

The above examples ......

.. code:: python
    session.solver.tui.define.boundary_conditions.fluid(
        "elbow-fluid",
        "yes",
        "water-liquid",
        "no",
        "no",
        "no",
        "no",
        "0",
        "no",
        "0",
        "no",
        "0",
        "no",
        "0",
        "no",
        "0",
        "no",
        "1",
        "no",
        "no",
        "no",
        "no",
        "no",
    )
