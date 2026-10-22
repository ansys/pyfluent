.. _ref_expression_builder_guide:

.. vale Google.Spacing = NO

Expression builder
==================

The expression builder allows you to construct Fluent expressions using Python instead of typing them by hand.
Use the :obj:`~ansys.fluent.core.offline.expressions.builder.ExpressionBuilder` class to build expressions
programmatically. This is useful for creating named expressions, field reductions, and other
expression-based features in your simulation.

Quick example
-------------

This example demonstrates how to construct an area-averaged pressure expression at an inlet:

.. code-block:: python

  >>> from ansys.fluent.core.offline.expressions import ExpressionBuilder
  >>> from ansys.units import VariableCatalog as V

  >>> builder = ExpressionBuilder()
  >>> expr = builder.reductions.area_ave(
  ...     expression=V.ABSOLUTE_PRESSURE, locations=["inlet1"]
  ... )

The resulting expression can be rendered and assigned to a named expression:

.. code-block:: python

  >>> str(expr)
  "AreaAve(AbsolutePressure,['inlet1'])"

  >>> named = solver.setup.named_expressions.create()
  >>> named.definition = expr
  >>> value = named.get_value()  # Retrieve the computed value
