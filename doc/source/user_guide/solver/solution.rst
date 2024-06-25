Apply solution settings
=======================

PyFluent allows you to use :ref:`ref_settings` to interact with solution settings, and initialize and solve.

Select solution method 
~~~~~~~~~~~~~~~~~~~~~~
This example demonstrates  how to select the pressure velocity coupling scheme and set the gradient
options. Five solution methods (Index-Model) are available: 20-SIMPLE, 21-SIMPLEC, 22-PISO, 24-Coupled, and 25-Fractional Step.
    
Select solution controls 
~~~~~~~~~~~~~~~~~~~~~~~~
This example demonstrates how to select pressure velocity controls.

Create report definition
~~~~~~~~~~~~~~~~~~~~~~~~
This example shows you how to create a report definition.

Initialize and solve 
~~~~~~~~~~~~~~~~~~~~
This example shows you how to initialize and perform a specified number of iterations.

**Python code**

.. code:: python

    solver.solution.initialization.hybrid_initialize()
    solver.solution.run_calculation.iterate(iter_count=150)
