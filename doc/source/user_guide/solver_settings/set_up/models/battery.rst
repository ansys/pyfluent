Battery model
=============

Setting up and querying the model
---------------------------------

.. code:: python

    >>> from ansys.fluent.core.solver import Battery
    >>> battery = Battery(settings_source=solver_session)
    >>> battery.enabled.set_state(True)
    >>> battery.solution_method.allowed_values()
    ['cht-coupling', 'fmu-cht-coupling', 'circuit-network', 'msmd', 'msmd-rom']