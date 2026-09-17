.. _ref_schemeeval_guide:

.. vale Google.Spacing = NO

Scheme code evaluation
======================

.. warning::

   PyFluent's modern, Pythonic interfaces provide stable, validated, high-level access to
   Fluent. Scheme access circumvents those interfaces, and as such, guarantees cannot be
   made about the outcome of making such calls. Note in particular that directly
   invoking a Scheme command via the interface shown here is not recorded in a Fluent
   Python journal.

Each session provides a :obj:`~ansys.fluent.core.session.base.BaseSession.scheme` property for executing Fluent's
scheme code.

Examples
--------

.. code-block:: python

   >>> session.scheme.exec(('(ti-menu-load-string "/report/system/proc-stats")',))
   >>> # Returns TUI output string
   >>> session.scheme.string_eval("(rpgetvar 'mom/relax)")
   '0.7'
   >>> session.scheme.eval("(+ 2 3)")
   5
   >>> session.scheme.eval("(rpgetvar 'mom/relax)")
   0.7
