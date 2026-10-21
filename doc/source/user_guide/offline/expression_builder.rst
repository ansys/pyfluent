.. _ref_expression_builder_guide:

.. vale Google.Spacing = NO

Expression builder
==================

The :obj:`~ansys.fluent.core.expressions.builder.ExpressionBuilder` class provides
a high-level, object-based API for constructing Fluent expression strings (for example,
``AreaAve(AbsolutePressure,['inlet1'])``) without hand-writing them. You can build
these expressions without a live Fluent session and later assign them to a solver's
named expressions or use them in other contexts.

Sample usage
------------

This example shows how to use the :obj:`~ansys.fluent.core.expressions.builder.ExpressionBuilder`
to construct a single-field reduction expression:

.. code-block:: python

  >>> from ansys.fluent.core.expressions import ExpressionBuilder
  >>> from ansys.units import VariableCatalog as V

  >>> builder = ExpressionBuilder()

  >>> expr = builder.reductions.area_ave(
  ...     expression=V.ABSOLUTE_PRESSURE, locations=["inlet1"]
  ... )
  >>> str(expr)
  "AreaAve(AbsolutePressure,['inlet1'])"

To assign this expression to a live solver session:

.. code-block:: python

  named = solver.setup.named_expressions.create()
  named.definition = expr
  val = named.get_value()
