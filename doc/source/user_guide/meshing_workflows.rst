.. _ref_user_guide_meshing_workflows:

Using the Meshing Workflows
===========================
PyFluent supports accessing all the Fluent Meshing functionalities including 
the guided Meshing Workflows.

Using the Watertight Geometry Meshing Workflow
----------------------------------------------
Here is a simple example demonstrating the the Watertight Geometry Workflow usage:

Importing Your Geometry
~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    import ansys.fluent.core as pyfluent
    from ansys.fluent.core import examples

    import_filename = examples.download_file('mixing_elbow.pmdb', 'pyfluent/mixing_elbow')
    session = pyfluent.launch_fluent(
        meshing_mode=True, precision='double', processor_count=2
    )
    session.meshing.workflow.InitializeWorkflow(WorkflowType='Watertight Geometry')
    session.meshing.workflow.TaskObject['Import Geometry'].Arguments = dict(
        FileName=import_filename, LengthUnit='in'
    )
    session.meshing.workflow.TaskObject['Import Geometry'].Execute()

Adding Local Sizing
~~~~~~~~~~~~~~~~~~~

.. code:: python

    session.meshing.workflow.TaskObject['Add Local Sizing'].AddChildToTask()
    session.meshing.workflow.TaskObject['Add Local Sizing'].Execute()

Generating the Surface Mesh
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    session.meshing.workflow.TaskObject['Generate the Surface Mesh'].Arguments = {
        'CFDSurfaceMeshControls': {'MaxSize': 0.3}
    }
    session.meshing.workflow.TaskObject['Generate the Surface Mesh'].Execute()

Describing the Geometry
~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    session.meshing.workflow.TaskObject['Describe Geometry'].UpdateChildTasks(
        SetupTypeChanged=False
    )
    session.meshing.workflow.TaskObject['Describe Geometry'].Arguments = dict(
        SetupType='The geometry consists of only fluid regions with no voids'
    )
    session.meshing.workflow.TaskObject['Describe Geometry'].UpdateChildTasks(
        SetupTypeChanged=True
    )
    session.meshing.workflow.TaskObject['Describe Geometry'].Execute()

Updating Boundaries
~~~~~~~~~~~~~~~~~~~

.. code:: python

    session.meshing.workflow.TaskObject['Update Boundaries'].Arguments = {
        'BoundaryLabelList': ['wall-inlet'],
        'BoundaryLabelTypeList': ['wall'],
        'OldBoundaryLabelList': ['wall-inlet'],
        'OldBoundaryLabelTypeList': ['velocity-inlet'],
    }
    session.meshing.workflow.TaskObject['Update Boundaries'].Execute()

Updating Regions
~~~~~~~~~~~~~~~~

.. code:: python

    session.meshing.workflow.TaskObject['Update Regions'].Execute()

Adding Boundary Layers
~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    session.meshing.workflow.TaskObject['Add Boundary Layers'].AddChildToTask()
    session.meshing.workflow.TaskObject['Add Boundary Layers'].InsertCompoundChildTask()
    session.meshing.workflow.TaskObject['smooth-transition_1'].Arguments = {
        'BLControlName': 'smooth-transition_1',
    }
    session.meshing.workflow.TaskObject['Add Boundary Layers'].Arguments = {}
    session.meshing.workflow.TaskObject['smooth-transition_1'].Execute()

Generating the Volume Mesh
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    session.meshing.workflow.TaskObject['Generate the Volume Mesh'].Arguments = {
        'VolumeFill': 'poly-hexcore',
        'VolumeFillControls': {
            'HexMaxCellLength': 0.3,
        },
    }
    session.meshing.workflow.TaskObject['Generate the Volume Mesh'].Execute()

Switching to Solution Mode
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    session.meshing.tui.switch_to_solution_mode('yes')

Using the Fault-tolerant Meshing Workflow
-----------------------------------------
Here is a simple example demonstrating the the Fault-tolerant Meshing Workflow usage:

Importing CAD and Part Management
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    import ansys.fluent.core as pyfluent
    from ansys.fluent.core import examples

    import_filename = examples.download_file(
        'exhaust_system.fmd', 'pyfluent/exhaust_system'
    )
    session = pyfluent.launch_fluent(
        meshing_mode=True, precision='double', processor_count=2
    )
    session.meshing.workflow.InitializeWorkflow(WorkflowType='Fault-tolerant Meshing')
    session.meshing.PartManagement.InputFileChanged(
        FilePath=import_filename, IgnoreSolidNames=False, PartPerBody=False
    )
    session.meshing.PMFileManagement.FileManager.LoadFiles()
    session.meshing.PartManagement.Node['Meshing Model'].Copy(
        Paths=[
            '/dirty_manifold-for-wrapper,' + '1/dirty_manifold-for-wrapper,1/main,1',
            '/dirty_manifold-for-wrapper,' + '1/dirty_manifold-for-wrapper,1/flow-pipe,1',
            '/dirty_manifold-for-wrapper,' + '1/dirty_manifold-for-wrapper,1/outpipe3,1',
            '/dirty_manifold-for-wrapper,' + '1/dirty_manifold-for-wrapper,1/object2,1',
            '/dirty_manifold-for-wrapper,' + '1/dirty_manifold-for-wrapper,1/object1,1',
        ]
    )
    session.meshing.PartManagement.ObjectSetting[
        'DefaultObjectSetting'
    ].OneZonePer.setState('part')
    session.meshing.workflow.TaskObject[
        'Import CAD and Part Management'
    ].Arguments.setState(
        {
            'Context': 0,
            'CreateObjectPer': 'Custom',
            'FMDFileName': import_filename,
            'FileLoaded': 'yes',
            'ObjectSetting': 'DefaultObjectSetting',
            'Options': {
                'Line': False,
                'Solid': False,
                'Surface': False,
            },
        }
    )
    session.meshing.workflow.TaskObject['Import CAD and Part Management'].Execute()

Describing Geometry and Flow
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    session.meshing.workflow.TaskObject['Describe Geometry and Flow'].Arguments.setState(
        {
            'AddEnclosure': 'No',
            'CloseCaps': 'Yes',
            'FlowType': 'Internal flow through the object',
        }
    )
    session.meshing.workflow.TaskObject['Describe Geometry and Flow'].UpdateChildTasks(
        SetupTypeChanged=False
    )
    session.meshing.workflow.TaskObject['Describe Geometry and Flow'].Arguments.setState(
        {
            'AddEnclosure': 'No',
            'CloseCaps': 'Yes',
            'DescribeGeometryAndFlowOptions': {
                'AdvancedOptions': True,
                'ExtractEdgeFeatures': 'Yes',
            },
            'FlowType': 'Internal flow through the object',
        }
    )
    session.meshing.workflow.TaskObject['Describe Geometry and Flow'].UpdateChildTasks(
        SetupTypeChanged=False
    )
    session.meshing.workflow.TaskObject['Describe Geometry and Flow'].Execute()

Enclosing Fluid Regions (Capping)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    session.meshing.workflow.TaskObject[
        'Enclose Fluid Regions (Capping)'
    ].Arguments.setState(
        {
            'CreatePatchPreferences': {
                'ShowCreatePatchPreferences': False,
            },
            'PatchName': 'inlet-1',
            'SelectionType': 'zone',
            'ZoneSelectionList': ['inlet.1'],
        }
    )
    session.meshing.workflow.TaskObject[
        'Enclose Fluid Regions (Capping)'
    ].Arguments.setState(
        {
            'CreatePatchPreferences': {
                'ShowCreatePatchPreferences': False,
            },
            'PatchName': 'inlet-1',
            'SelectionType': 'zone',
            'ZoneLocation': [
                '1',
                '351.68205',
                '-361.34322',
                '-301.88668',
                '396.96205',
                '-332.84759',
                '-266.69751',
                'inlet.1',
            ],
            'ZoneSelectionList': ['inlet.1'],
        }
    )
    session.meshing.workflow.TaskObject['Enclose Fluid Regions (Capping)'].AddChildToTask()

    session.meshing.workflow.TaskObject[
        'Enclose Fluid Regions (Capping)'
    ].InsertCompoundChildTask()
    session.meshing.workflow.TaskObject[
        'Enclose Fluid Regions (Capping)'
    ].Arguments.setState({})
    session.meshing.workflow.TaskObject['inlet-1'].Execute()
    session.meshing.workflow.TaskObject[
        'Enclose Fluid Regions (Capping)'
    ].Arguments.setState(
        {
            'PatchName': 'inlet-2',
            'SelectionType': 'zone',
            'ZoneSelectionList': ['inlet.2'],
        }
    )
    session.meshing.workflow.TaskObject[
        'Enclose Fluid Regions (Capping)'
    ].Arguments.setState(
        {
            'PatchName': 'inlet-2',
            'SelectionType': 'zone',
            'ZoneLocation': [
                '1',
                '441.68205',
                '-361.34322',
                '-301.88668',
                '486.96205',
                '-332.84759',
                '-266.69751',
                'inlet.2',
            ],
            'ZoneSelectionList': ['inlet.2'],
        }
    )
    session.meshing.workflow.TaskObject['Enclose Fluid Regions (Capping)'].AddChildToTask()

    session.meshing.workflow.TaskObject[
        'Enclose Fluid Regions (Capping)'
    ].InsertCompoundChildTask()
    session.meshing.workflow.TaskObject[
        'Enclose Fluid Regions (Capping)'
    ].Arguments.setState({})
    session.meshing.workflow.TaskObject['inlet-2'].Execute()
    session.meshing.workflow.TaskObject[
        'Enclose Fluid Regions (Capping)'
    ].Arguments.setState(
        {
            'PatchName': 'inlet-3',
            'SelectionType': 'zone',
            'ZoneSelectionList': ['inlet'],
        }
    )
    session.meshing.workflow.TaskObject[
        'Enclose Fluid Regions (Capping)'
    ].Arguments.setState(
        {
            'PatchName': 'inlet-3',
            'SelectionType': 'zone',
            'ZoneLocation': [
                '1',
                '261.68205',
                '-361.34322',
                '-301.88668',
                '306.96205',
                '-332.84759',
                '-266.69751',
                'inlet',
            ],
            'ZoneSelectionList': ['inlet'],
        }
    )
    session.meshing.workflow.TaskObject['Enclose Fluid Regions (Capping)'].AddChildToTask()

    session.meshing.workflow.TaskObject[
        'Enclose Fluid Regions (Capping)'
    ].InsertCompoundChildTask()
    session.meshing.workflow.TaskObject[
        'Enclose Fluid Regions (Capping)'
    ].Arguments.setState({})
    session.meshing.workflow.TaskObject['inlet-3'].Execute()
    session.meshing.workflow.TaskObject[
        'Enclose Fluid Regions (Capping)'
    ].Arguments.setState(
        {
            'PatchName': 'outlet-1',
            'SelectionType': 'zone',
            'ZoneSelectionList': ['outlet'],
            'ZoneType': 'pressure-outlet',
        }
    )
    session.meshing.workflow.TaskObject[
        'Enclose Fluid Regions (Capping)'
    ].Arguments.setState(
        {
            'PatchName': 'outlet-1',
            'SelectionType': 'zone',
            'ZoneLocation': [
                '1',
                '352.22702',
                '-197.8957',
                '84.102381',
                '394.41707',
                '-155.70565',
                '84.102381',
                'outlet',
            ],
            'ZoneSelectionList': ['outlet'],
            'ZoneType': 'pressure-outlet',
        }
    )
    session.meshing.workflow.TaskObject['Enclose Fluid Regions (Capping)'].AddChildToTask()

    session.meshing.workflow.TaskObject[
        'Enclose Fluid Regions (Capping)'
    ].InsertCompoundChildTask()
    session.meshing.workflow.TaskObject[
        'Enclose Fluid Regions (Capping)'
    ].Arguments.setState({})
    session.meshing.workflow.TaskObject['outlet-1'].Execute()

Extracting Edge Features
~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    session.meshing.workflow.TaskObject['Extract Edge Features'].Arguments.setState(
        {
            'ExtractMethodType': 'Intersection Loops',
            'ObjectSelectionList': ['flow_pipe', 'main'],
        }
    )
    session.meshing.workflow.TaskObject['Extract Edge Features'].AddChildToTask()

    session.meshing.workflow.TaskObject['Extract Edge Features'].InsertCompoundChildTask()

    session.meshing.workflow.TaskObject['edge-group-1'].Arguments.setState(
        {
            'ExtractEdgesName': 'edge-group-1',
            'ExtractMethodType': 'Intersection Loops',
            'ObjectSelectionList': ['flow_pipe', 'main'],
        }
    )
    session.meshing.workflow.TaskObject['Extract Edge Features'].Arguments.setState({})

    session.meshing.workflow.TaskObject['edge-group-1'].Execute()

Identifying Regions
~~~~~~~~~~~~~~~~~~~

.. code:: python

    session.meshing.workflow.TaskObject['Identify Regions'].Arguments.setState(
        {
            'SelectionType': 'zone',
            'X': 377.322045740589,
            'Y': -176.800676988458,
            'Z': -37.0764628583475,
            'ZoneSelectionList': ['main.1'],
        }
    )
    session.meshing.workflow.TaskObject['Identify Regions'].Arguments.setState(
        {
            'SelectionType': 'zone',
            'X': 377.322045740589,
                'Y': -176.800676988458,
            'Z': -37.0764628583475,
            'ZoneLocation': [
                '1',
                '213.32205',
                '-225.28068',
                '-158.25531',
                '541.32205',
                '-128.32068',
                '84.102381',
                'main.1',
            ],
            'ZoneSelectionList': ['main.1'],
        }
    )
    session.meshing.workflow.TaskObject['Identify Regions'].AddChildToTask()

    session.meshing.workflow.TaskObject['Identify Regions'].InsertCompoundChildTask()

    session.meshing.workflow.TaskObject['fluid-region-1'].Arguments.setState(
        {
            'MaterialPointsName': 'fluid-region-1',
            'SelectionType': 'zone',
            'X': 377.322045740589,
            'Y': -176.800676988458,
            'Z': -37.0764628583475,
            'ZoneLocation': [
                '1',
                '213.32205',
                '-225.28068',
                '-158.25531',
                '541.32205',
                '-128.32068',
                '84.102381',
                'main.1',
            ],
            'ZoneSelectionList': ['main.1'],
        }
    )
    session.meshing.workflow.TaskObject['Identify Regions'].Arguments.setState({})

    session.meshing.workflow.TaskObject['fluid-region-1'].Execute()
    session.meshing.workflow.TaskObject['Identify Regions'].Arguments.setState(
        {
            'MaterialPointsName': 'void-region-1',
            'NewRegionType': 'void',
            'ObjectSelectionList': ['inlet-1', 'inlet-2', 'inlet-3', 'main'],
            'X': 374.722045740589,
            'Y': -278.9775145640143,
            'Z': -161.1700719416913,
        }
    )
    session.meshing.workflow.TaskObject['Identify Regions'].AddChildToTask()

    session.meshing.workflow.TaskObject['Identify Regions'].InsertCompoundChildTask()

    session.meshing.workflow.TaskObject['Identify Regions'].Arguments.setState({})

    session.meshing.workflow.TaskObject['void-region-1'].Execute()

Defining Leakage Threshold
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    session.meshing.workflow.TaskObject['Define Leakage Threshold'].Arguments.setState(
        {
            'AddChild': 'yes',
            'FlipDirection': True,
            'PlaneDirection': 'X',
            'RegionSelectionSingle': 'void-region-1',
        }
    )
    session.meshing.workflow.TaskObject['Define Leakage Threshold'].AddChildToTask()

    session.meshing.workflow.TaskObject[
        'Define Leakage Threshold'
    ].InsertCompoundChildTask()
    session.meshing.workflow.TaskObject['leakage-1'].Arguments.setState(
        {
            'AddChild': 'yes',
            'FlipDirection': True,
            'LeakageName': 'leakage-1',
            'PlaneDirection': 'X',
            'RegionSelectionSingle': 'void-region-1',
        }
    )
    session.meshing.workflow.TaskObject['Define Leakage Threshold'].Arguments.setState(
        {
            'AddChild': 'yes',
        }
    )
    session.meshing.workflow.TaskObject['leakage-1'].Execute()

Updating Regions Settings
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    session.meshing.workflow.TaskObject['Update Region Settings'].Arguments.setState(
        {
            'AllRegionFilterCategories': ['2'] * 5 + ['1'] * 2,
            'AllRegionLeakageSizeList': ['none'] * 6 + ['6.4'],
            'AllRegionLinkedConstructionSurfaceList': ['n/a'] * 6 + ['no'],
            'AllRegionMeshMethodList': ['none'] * 6 + ['wrap'],
            'AllRegionNameList': [
                'main',
                'flow_pipe',
                'outpipe3',
                'object2',
                'object1',
                'void-region-1',
                'fluid-region-1',
            ],
            'AllRegionOversetComponenList': ['no'] * 7,
            'AllRegionSourceList': ['object'] * 5 + ['mpt'] * 2,
            'AllRegionTypeList': ['void'] * 6 + ['fluid'],
            'AllRegionVolumeFillList': ['none'] * 6 + ['tet'],
            'FilterCategory': 'Identified Regions',
            'OldRegionLeakageSizeList': [''],
            'OldRegionMeshMethodList': ['wrap'],
            'OldRegionNameList': ['fluid-region-1'],
            'OldRegionOversetComponenList': ['no'],
            'OldRegionTypeList': ['fluid'],
            'OldRegionVolumeFillList': ['hexcore'],
            'RegionLeakageSizeList': [''],
            'RegionMeshMethodList': ['wrap'],
            'RegionNameList': ['fluid-region-1'],
            'RegionOversetComponenList': ['no'],
            'RegionTypeList': ['fluid'],
            'RegionVolumeFillList': ['tet'],
        }
    )
    session.meshing.workflow.TaskObject['Update Region Settings'].Execute()


Choosing Mesh Control Options
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    session.meshing.workflow.TaskObject['Choose Mesh Control Options'].Execute()

Generating the Surface Mesh
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    session.meshing.workflow.TaskObject['Generate the Surface Mesh'].Execute()

Updating Boundaries
~~~~~~~~~~~~~~~~~~~

.. code:: python

    session.meshing.workflow.TaskObject['Update Boundaries'].Execute()

Adding Boundary Layers
~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    session.meshing.workflow.TaskObject['Add Boundary Layers'].AddChildToTask()

    session.meshing.workflow.TaskObject['Add Boundary Layers'].InsertCompoundChildTask()

    session.meshing.workflow.TaskObject['aspect-ratio_1'].Arguments.setState(
        {
            'BLControlName': 'aspect-ratio_1',
        }
    )
    session.meshing.workflow.TaskObject['Add Boundary Layers'].Arguments.setState({})

    session.meshing.workflow.TaskObject['aspect-ratio_1'].Execute()

Generating the Volume Mesh
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    session.meshing.workflow.TaskObject['Generate the Volume Mesh'].Arguments.setState(
        {
            'AllRegionNameList': [
                'main',
                'flow_pipe',
                'outpipe3',
                'object2',
                'object1',
                'void-region-1',
                'fluid-region-1',
            ],
            'AllRegionSizeList': ['11.33375'] * 7,
            'AllRegionVolumeFillList': ['none'] * 6 + ['tet'],
            'EnableParallel': True,
        }
    )
    session.meshing.workflow.TaskObject['Generate the Volume Mesh'].Execute()

Switching to Solution Mode
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    session.meshing.tui.switch_to_solution_mode('yes')