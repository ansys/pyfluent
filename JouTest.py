try:
    import ansys.fluent.core as pyfluent

    flglobals = pyfluent.setup_for_fluent(
        product_version="23.1.0", mode="meshing", version="2d", precision="double"
    )
    globals().update(flglobals)
except Exception:
    pass
workflow.Workflow.TaskList.set_state(None)
workflow.set_state(
    {
        r"TaskObject:Import Geometry": None,
    }
)
workflow.set_state(
    {
        r"TaskObject:Add Local Sizing": None,
    }
)
workflow.set_state(
    {
        r"TaskObject:Generate the Surface Mesh": None,
    }
)
workflow.set_state(
    {
        r"TaskObject:Describe Geometry": None,
    }
)
workflow.set_state(
    {
        r"TaskObject:Apply Share Topology": None,
    }
)
workflow.set_state(
    {
        r"TaskObject:Enclose Fluid Regions (Capping)": None,
    }
)
workflow.set_state(
    {
        r"TaskObject:Update Boundaries": None,
    }
)
workflow.set_state(
    {
        r"TaskObject:Create Regions": None,
    }
)
workflow.set_state(
    {
        r"TaskObject:Update Regions": None,
    }
)
workflow.set_state(
    {
        r"TaskObject:Add Boundary Layers": None,
    }
)
workflow.set_state(
    {
        r"TaskObject:Generate the Volume Mesh": None,
    }
)
workflow.set_state(
    {
        r"TaskObject:smooth-transition_1": None,
    }
)
meshing.GlobalSettings.LengthUnit.set_state(r"mm")
workflow.LoadState(ListOfRoots=[r"meshing", r"workflow"])
