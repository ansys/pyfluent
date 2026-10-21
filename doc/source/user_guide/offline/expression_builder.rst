.. _ref_expression_builder_guide:

Expression builder
==================

The expression builder allows you to construct Fluent expressions using Python instead of typing them by hand.
Use the :obj:`~ansys.fluent.core.offline.expressions.builder.ExpressionBuilder` class to build expressions
programmatically. This is useful for creating named expressions, field reductions, and other
expression-based features in your simulation.

Sample usage
------------

This example shows how to use the :obj:`~ansys.fluent.core.expressions.builder.ExpressionBuilder`
to construct an expression computing the pressure drop across two surfaces:

.. code-block:: python

  >>> from ansys.fluent.core.offline.expressions import ExpressionBuilder
  >>> from ansys.units import VariableCatalog as V

  >>> builder = ExpressionBuilder()

  >>> inlet = builder.reductions.area_ave(
  ...     expression=V.ABSOLUTE_PRESSURE, locations=["inlet1"]
  ... )
  >>> outlet = builder.reductions.area_ave(
  ...     expression=V.ABSOLUTE_PRESSURE, locations=["outlet"]
  ... )
  >>> dp = inlet - outlet

  >>> str(dp)
  "(AreaAve(AbsolutePressure,['inlet1']) - AreaAve(AbsolutePressure,['outlet']))"

To assign this expression to a live solver session, use:

.. code-block:: python

  solver.setup.named_expressions["dp"] = {}
  solver.setup.named_expressions["dp"].definition = str(dp)
