

def run():
    import ansys.fluent as pyfluent
    session = pyfluent.launch_fluent(meshing_mode=True)
    w = session.workflow
    status=w.initialize_workflow(WorkflowType="Watertight Geometry")
    w.task_object['Import Geometry'].arguments = {"FileName":"E:/x.scdoc.pmdb","AppendMesh":False}
    w.task_object['Import Geometry'].execute()
    w.task_object['Add Local Sizing'].arguments = {"AddChild":"yes", "BOIControlName":"face", "BOIExecution":"Body Size", "BOIFaceLabelList":"farfield", "BOIZoneorLabel":"label"}
    status=w.task_object['Add Local Sizing'].execute()
    status=w.task_object['Add Local Sizing'].insert_compound_child_task()
    w.task_object['Add Local Sizing'].arguments.update_dict({"AddChild":"yes"})
    w.task_object['face'].arguments.update_dict({"AddChild":"yes", "BOIControlName":"refinementzone", "BOIExecution":"Body Size", "BOIFaceLabelList":"meshrefinement", "BOISize":60})
    status=w.task_object['Generate the Surface Mesh'].execute()
    status=w.task_object['Generate the Surface Mesh'].insert_next_task(command_name='SurfaceMeshImprove')
    w.task_object['Improve Surface Mesh'].arguments.update_dict({'FaceQualityLimit':0.7, 'MeshObject':'', 'SMImprovePreferences':{"SIQualityMaxAngle":160,"SIQualityIterations":5,"SIQualityCollapseLimit":0.85}})
    status=w.task_object['Improve Surface Mesh'].execute()
    w.task_object['Describe Geometry'].arguments.update_dict({'CappingRequired':'No', 'InvokeShareTopology':'No', 'SetupInternalTypes': None, 'SetupInternals': None, 'SetupType': 'The geometry consists of both fluid and solid regions and/or voids', 'WallToInternal':'Yes'})
    status=w.task_object['Describe Geometry'].execute()
    status=w.task_object['Update Boundaries'].execute()
    w.task_object['Create Regions'].arguments.update_dict({'NumberOfFlowVolumes':2})
    status=w.task_object['Create Regions'].execute()
    status=w.task_object['Update Regions'].execute()
    w.task_object['Add Boundary Layers'].add_child_to_task()
    w.task_object['Add Boundary Layers'].insert_compound_child_task()
    w.task_object['smooth-transition_1'].arguments.update_dict({'BLControlName':'smooth-transition_1','NumberOfLayers':10, "OffsetMethodType":'smooth-transition',"transition_ratio":0.272})
    status=w.task_object['Add Boundary Layers'].execute()
    w.task_object['Generate the Volume Mesh'].arguments.update_dict({'VolumeFill':'polyhedra'})
    w.task_object['Generate the Volume Mesh'].execute().result()
    return session
