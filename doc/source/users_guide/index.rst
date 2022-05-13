
.. _user_guide:

************
User's Guide
************
This guide contains pertinent information regarding using Ansys PyFluent and its
constituent modules and components.

==================================
Understanding the PyFluent Modules
==================================
Session objects are the main entry point when using the PyFluent library, where
one or more Fluent client sessions can be launched simulateously from the
server. For example:

.. code:: python

   solver_session = pyfluent.launch_fluent()

or

.. code:: python

   meshing_session = pyfluent.launch_fluent(meshing_mode=True)

Each session object provides access to multiple services, such as boundary
contitions, meshing workflows, field data properties, and so forth.

PyFluent contains several basic service modules that provide access to core
Fluent capabilities. 

   - General command and query services are encompassed in three modules: 

      + The 'tui' modules are a collection of Python wrappers around the
        Fluent's traditional Text User Interface (TUI) command-based
        infrastructure.

      .. code::

         solver_session.tui.define.models.unsteady_2nd_order('yes’)​

      + The 'settings' module is a Pythonic interface to access Fluent's setup
        and solution objects, where you can, for instance, enable a
        physics-based model for your simulation.

      .. code::

         session.solver.root.setup.models.energy.enabled = True

      + The 'datamodel' module is a Python interface to access the
        datamodel-driven aspects of Fluent, such as the meshing workflows.

      .. code::

         import_geometry.arguments.update_dict({'AppendMesh':True})

   - Surface field and mesh data services are available using the 'field_data'
     module, such as obtaining surface data for a specified surface.

   .. code:: 

      surface_data = field_data.get_surfaces(surface_ids)​

   - There are general modules available, such as 'health_check', 'transcript',
     and 'events' that provide access to generic features that are useful to
     running your simulation. For instance,

   .. code:: 

      health_check_service.check_health()​​

   or

   .. code:: 

      transcript_service.begin_streaming()​​

   or

   .. code:: 

      events_service.begin_streaming()

   - Finally, there is a 'scheme_eval' module that provides access to Scheme
     function evaluation. For instance,

   .. code:: 

      scheme_eval.string_eval("(rp-unsteady?)")​

