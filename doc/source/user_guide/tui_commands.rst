.. _ref_user_guide_tui_commands:

Use TUI commands
================

TUI commands refer to a programming interface that mirrors the Fluent TUI (text
user interface). There is a TUI command hierarchy defined for each of the two
modes: meshing and solution. The hierarchy that is active depends on the current
Fluent mode. The guidance in this topic applies to both modes.

The PyFluent TUI commands allow you to automate workflows. Everything that's in
the Fluent TUI (which itself is a comprehensive automation interface) is exposed
in PyFluent. The PyFluent TUI commands are Pythonic versions of the commands
that are used in the Fluent console.

The PyFluent TUI commands do not support TUI features such as aliases or
command abbreviation. To make using PyFluent commands in an interactive
session easier, you can install a tool such as
`pyreadline3 <https://github.com/pyreadline3/pyreadline3>`_, which provides
both command line completion and history. To inspect any PyFluent TUI object further,
you can use the Python built-in `help <https://docs.python.org/3/library/functions.html#help>`_
and `dir <https://docs.python.org/3/library/functions.html#dir>`_ functions.
For example, to see the options available under the viscous model menu, the
following can be used, assuming that ``solver`` is the session instance returned
by ``launch_fluent``:

.. code-block:: python

   >>> dir(solver.tui.define.models.viscous)
   ['add_intermittency_transition_model', 'add_transition_model',
   'corner_flow_correction', 'curvature_correction',
   'detached_eddy_simulation', 'inviscid', 'k_kl_w', 'ke_realizable', 'ke_rng',
   'ke_standard', 'kw_bsl', 'kw_geko', 'kw_low_re_correction', 'kw_sst',
   'kw_standard', 'kw_wj_bsl_earsm', 'laminar', 'large_eddy_simulation',
   'mixing_length', 'near_wall_treatment', 'reynolds_stress_model', 'sas',
   'spalart_allmaras', 'transition_sst', 'turbulence_expert', 'user_defined']

To see the documentation for the viscous model menu options, you can run:

.. code-block:: python

   >>> help(solver.tui.define.models.viscous)
   Help on viscous in module ansys.fluent.core.solver.tui_241 object:

   class viscous(ansys.fluent.core.services.datamodel_tui.TUIMenu)
    |  viscous(service, version, mode, path)
    |
    |  Enters the viscous model menu.
    |
    |  Method resolution order:
    |      viscous
    |      ansys.fluent.core.services.datamodel_tui.TUIMenu
    |      builtins.object
    |
    |  Methods defined here:
    |
    |  __init__(self, service, version, mode, path)
    |      __init__ method of TUIMenu class.
    |
    |  add_intermittency_transition_model(self, *args, **kwargs)
    |      Enable/disable the intermittency transition model to account for transitional effects.
   ...

The arguments to a TUI command are those that would be passed in direct
interaction in the Fluent console, but they are in a Pythonic style. In the recent
Fluent versions, in both meshing and solution mode,
you can use Python journaling, which is a beta feature,
to construct the TUI commands for PyFluent. The following section describes how to
construct the TUI commands for PyFluent in different Fluent versions.

TUI command construction
------------------------

From the 2023 R2 release onward, a Fluent Python journal contains Python calls
corresponding to the TUI commands executed in Fluent. Python journaling generates
a call to a corresponding settings API command if one exists. For instance, with Fluent
running in solution mode and Python journaling started, you can type the following in
the Fluent console to set velocity inlet properties:

.. code:: scheme

   /define/boundary_conditions/set/velocity-inlet

This command instigates a sequence of prompts in the console. Assume that your responses
to each prompt are as follows:

.. code:: scheme

   velocity-inlet-5
   ()
   temperature
   no
   293.15
   quit

The following code yields the same result but specifies all arguments in one call:

.. code:: scheme

   /define/boundary-conditions/set/velocity-inlet velocity-inlet-5 () temperature no 293.15 quit

The recorded Python journal contains the following line which can be executed in
PyFluent, assuming ``solver`` is the session instance returned by ``launch_fluent``.

.. code:: python

   solver.setup.boundary_conditions.velocity_inlet['inlet1'] = {"t" : 293.15}

In the above example, the settings API command is recorded as that exists for the TUI
command. An example where settings API doesn't exist is setting the pressure unit:

.. code:: scheme

    /define/units pressure "Pa"

The corresponding Python command recorded in the Python journal is:

.. code:: python

   solver.tui.define.units('pressure', '"Pa"')

Note, the string ``"Pa"`` is wrapped in single quotation marks
to preserve the double quotation marks around the TUI argument.

A command line flag ``-topy`` is also available in Fluent to convert an existing
Fluent journal to Python journal. The following command writes a Python journal
file my_journal.py in the working directory.

.. code:: console

   fluent.exe 3ddp -i my_journal.jou -topy


In Fluent 2023 R1, the TUI commands for which settings API exist are recorded
as settings API commands in the Python journal. All other TUI commands are recorded
in a manner which is not Pythonic. You need to manually convert those TUI commands
using the transformation rules described in the next section.

In Fluent 2022 R2, Python journaling feature is not available. You need to manually
convert the TUI commands using the transformation rules described in the next section.

TUI command transformation rules
--------------------------------
The following rules are implied in the preceding examples:

- Each forward slash separator between elements in TUI paths is transformed to
  Python dot notation.
- Some characters in path elements are either removed or replaced because they
  are illegal inside Python names. For example:

  - Each hyphen in a path element is transformed to an underscore.
  - Each question mark in a path element is removed.

- Here are some rules about strings:

  - String-type arguments must be surrounded by quotation marks in Python.
  - A target Fluent TUI argument that is surrounded by quotation marks (like
    ``"Pa"`` in the preceding example) must be wrapped in single quotation marks
    so that the original quotation marks are preserved.
  - The contents of string arguments are preserved.

For more examples of TUI command usage, see :ref:`ref_mixing_elbow_tui_api`.
