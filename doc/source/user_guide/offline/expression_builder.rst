.. _ref_expression_builder_guide:

Expression builder
==================

The :obj:`~ansys.fluent.core.expressions.builder.ExpressionBuilder` class provides
a high-level, object-based API for constructing Fluent expression strings
(for example, ``AreaAve(AbsolutePressure,['inlet1'])``) without hand-writing them.
You can use the expression builder without a live Fluent session to build expressions
that you later assign to a solver's named expressions or use in other contexts.

Sample usage
------------

This example shows how to use the :obj:`~ansys.fluent.core.expressions.builder.ExpressionBuilder`
to construct an expression computing the pressure drop across two surfaces:

.. code-block:: python

  >>> from ansys.fluent.core.expressions import ExpressionBuilder
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
