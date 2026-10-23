.. _ref_expression_builder_guide:

.. vale Google.Spacing = NO

Expression builder
==================

The expression builder allows you to construct Fluent expressions using Python 
instead of typing them by hand. Use the 
:obj:`~ansys.fluent.core.offline.expressions.builder.ExpressionBuilder` class 
to build expressions programmatically. This is useful for creating named 
expressions, field reductions, and other expression-based features in your 
simulation.

To assign the expression to a named expression in a live Fluent solver:

.. code-block:: python

  >>> from ansys.fluent.core import Solver
  >>> from ansys.fluent.core.examples import download_file
  >>> from ansys.fluent.core.offline.expressions import ExpressionBuilder
  >>> from ansys.units import VariableCatalog as V

  >>> solver_session = Solver.from_install()
  >>> case_path = download_file("Static_Mixer_main.cas.h5", "pyfluent/static_mixer")
  >>> solver_session.settings.file.read_case(file_name=case_path)

  >>> # Initialize the solution before creating and evaluating expressions
  >>> solver_session.solution.initialization.hybrid_initialize()

  >>> # Create the expression builder
  >>> builder = ExpressionBuilder(session=solver_session)
  >>> expr = builder.reductions.area_ave(
  ...     expression=V.ABSOLUTE_PRESSURE, locations=["inlet1"]
  ... )

  >>> # Assign to a named expression and evaluate
  >>> # The expression is converted to string format: "AreaAve(AbsolutePressure,['inlet1'])"
  >>> named = solver_session.settings.setup.named_expressions.create()
  >>> named.definition = expr
  >>> # Call get_value() to evaluate the expression against the flow field using Fluent's solver
  >>> value = named.get_value()
