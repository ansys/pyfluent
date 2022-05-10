
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

To launch Ansys Fluent in meshing mode, double precision:

.. image:: ./launch_fluent_meshing_dp_t2.png
  :width: 800
  :alt: Launch Fluent in meshing mode in double precision, number of processors = 2

.. code:: python

   meshing_session = pyfluent.launch_fluent(meshing_mode=True, precision='double')

or, to launch Ansys Fluent in solver mode, 2d, double precision, number of prcessors = 2

.. image:: ./launch_fluent_2ddp_t2.png
  :width: 800
  :alt: Launch Fluent in solver mode, 2d, double precision, number of processors = 2

.. code:: python

   solver_session = pyfluent.launch_fluent(precision='double', processor_count=2, version='2d')

Each session object provides access to multiple services, such as meshing workflows, setup,
solutoin, parametric study, postprocessing, field data properties, and so forth.

PyFluent contains several basic service modules that provide access to core
Fluent capabilities. General command and query services are encompassed in three modules: 

The 'datamodel' module is a Python interface to access the datamodel-driven aspects of Fluent,
such as the meshing workflows. For example: To initialize watertight meshing workflow and to
import a geometry.

.. image:: ./wtm_import_geometry.png
  :width: 800
  :alt: Initialize watertight meshing workflow and import geometry

.. code::

   session.workflow.InitializeWorkflow(WorkflowType='Watertight Geometry')
   session.workflow.TaskObject['Import Geometry'].Arguments = dict(
       FileName=import_filename, LengthUnit='in'
   )
   session.workflow.TaskObject['Import Geometry'].Execute()

The 'tui' modules are a collection of Python wrappers around the Fluent's traditional Text User
Interface (TUI) command-based infrastructure.
For example: To import a case file and enable unsteady 2nd order model.

 .. image:: ./tui_import_case_2nd_unsteady_model.png
   :width: 800
   :alt: Import case, enable 2nd order unsted model

.. code::

   session.tui.solver.file.read_case(case_file_name='elbow.cas.h5')
   session.tui.solver.define.models.unsteady_2nd_order('yes')

The 'settings' module (Beta) is a Pythonic interface to access Fluent's setup
and solution objects.
For example: To enable energy equation, define boundary conditions and to create
report definitions. 

 .. image:: ./settings_setup_solution.png
   :width: 800
   :alt: Enable energy equation, define boundary conditions

.. code::

   settings= session.get_settings_root()
   settings.setup.models.energy.enabled = True
   settings.setup.boundary_conditions.velocity_inlet['cold-inlet'].vmag = {
       'option': 'constant or expression',
       'constant': 0.5,
   }
   settings.solution.report_definitions.surface['velocity_magnitude_outlet'] = {}
   settings.solution.report_definitions.surface[
       'velocity_magnitude_outlet'
   ].report_type = 'surface-areaavg'
   settings.solution.report_definitions.surface[
       'velocity_magnitude_outlet'
   ].field = 'velocity-magnitude'
   settings.solution.report_definitions.surface[
       'velocity_magnitude_outlet'
   ].surface_names = ['outlet']

Surface field and mesh data services are available using the 'field_data' module, such
as obtaining surface data for a specified surface.

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

