.. _ref_schemeeval_guide:

.. vale Google.Spacing = NO

Scheme code evaluation
======================

Each session provides an instance of :obj:`~ansys.fluent.core.services.scheme_eval.SchemeEval` on which Fluent's
scheme code can be executed.

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
