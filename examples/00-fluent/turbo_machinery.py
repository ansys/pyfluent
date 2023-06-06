""".. _xxx:

Turbomachinery Setup and Analysis Using the Turbo Workflow
----------------------------------------------------------
This example sets up and solves a three-dimensional fluid flow through the
first three rows of a one and a half stage axial compressor, courtesy of
TFD Hannover. The compressor configuration is encountered in the aerospace
and turbomachinery industry. It is often important to predict the flow field
through the various components of a compressor in order to properly design
the turbomachine.

This example uses the guided workflow for turbomachinery setup and analysis
because it is appropriate for describing the type of turbo machine and its
configuration, importing the geometry, and defining turbo-related mappings
and physics conditions, before finally creating a turbo-specific topology
and reporting tools.

**Workflow tasks**

The Turbomachinery Setup and Analysis Using the Turbo Workflow guides you through these tasks:

- Describe and configure the turbomachinery
- Import the turbo-specific geometry
- Define the turbo-related mappings and physics conditions
- Create turbo-specific topology and reporting tools for postprocessing

**Problem description**

The first three rows of the 4.5 stage axial Hannover compressor (Courtesy of TFD Hannover) have an
inlet guide vane, rotor and stator. The inlet guide vane has 26 vanes, the rotor has 23 blades and
rotates at a velocity of 17,100 RPM and the stator has 30 passages. The total pressure at the inlet
is 60,000 Pa and a radial equilibrium distribution of static pressure at the outlet, with a static
pressure of 60500 Pa at the outlet along the hub.
"""

# sphinx_gallery_thumbnail_path = '_static/turbo_machinery.png'

###############################################################################
# Example Setup
# -------------
# Before you can use the turbo workflow, you must set up the
# example and initialize this workflow.
#
# Perform required imports
# ~~~~~~~~~~~~~~~~~~~~~~~~
# Perform required imports, which includes downloading and importing
# the geometry files.

import ansys.fluent.core as pyfluent
from ansys.fluent.core import examples

inlet_guide_vane_file, rotor_file, stator_file = [
    examples.download_file(CAD_file, "pyfluent/turbo_workflow")
    for CAD_file in ["IGV.gtm", "R1.gtm", "S1.gtm"]
]

###############################################################################
# Launch Fluent
# ~~~~~~~~~~~~~
# Launch Fluent as a service in solver mode with double precision running on
# four processors.

solver_session = pyfluent.launch_fluent(
    precision="double", processor_count=4, mode="solver"
)

###############################################################################
# Initialize workflow
# ~~~~~~~~~~~~~~~~~~~
# Initialize the turbo workflow.

solver_session.solverworkflow.GlobalSettings.EnableTurboMeshing()

###############################################################################
# Edit turbo-related preferences
# ------------------------------
# The Turbo Workflow partially involves setting up an association between cell
# and face zones and their proper region assignments in the turbo topology.
# For turbo-related geometries with a large number of components, these mappings
# can be more easily automated and optimized using Preferences where you can
# instruct Fluent to look for certain string configurations and in a certain order.
#
# Updating inlet region
# ~~~~~~~~~~~~~~~~~~~~~
# Change the default value to: *inflow*, *in*

solver_session.preferences.TurboWorkflow.FaceZoneSettings.InletRegion("*inflow* *in*")

###############################################################################
# Updating outlet region
# ~~~~~~~~~~~~~~~~~~~~~~
# Change the default value to: *outflow*, *out*

solver_session.preferences.TurboWorkflow.FaceZoneSettings.OutletRegion(
    "*outflow* *out*"
)

###############################################################################
# Updating periodic 1 region
# ~~~~~~~~~~~~~~~~~~~~~~~~~~
# Change the default value to: "*per*1*, *per*"

solver_session.preferences.TurboWorkflow.FaceZoneSettings.Periodic1Region(
    "*per*1* *per*"
)

###############################################################################
# Updating search order
# ~~~~~~~~~~~~~~~~~~~~~
# Change the default value to:
# *int*, *def*, *bld*, *blade*, *tip*2*, *tip*b*, *tip*out*, *tip*, *sym*,
# *per*1*, *per*2*, *per*b*, *high*per*, *per*, *hub*, *shr*, *cas*, *inflow*, *outflow*,
# *in*, *out*

solver_session.preferences.TurboWorkflow.FaceZoneSettings.FZSearchOrder(
    "*int* *def* *bld* *blade* *tip*2* *tip*b* *tip*out* *tip* *sym* *per*1* *per*2* *per*b* *high*per* *per* *hub* *shr* *cas* *inflow* *outflow* *in* *out*"
)

###############################################################################
# Define workflow tasks
# ---------------------
#
# Describe component
# ~~~~~~~~~~~~~~~~~~
# Describe the turbomachinery component.

solver_session.solverworkflow.TWF_BasicMachineDescription(
    ComponentType="Axial Compressor",
    ComponentName="hannover",
    NumRows=3,
    RowNumList=["row 1", "row 2", "row 3"],
    OldRowNameList=["stator_1", "rotor_1", "stator_2"],
    NewRowNameList=["igv", "r1", "s1"],
    OldRowTypeList=["stationary", "rotating", "stationary"],
    NewRowTypeList=["stationary", "rotating", "stationary"],
    OldNumOfBladesList=["3", "3", "3"],
    NewNumOfBladesList=["26", "23", "30"],
    OldEnableTipGapList=["no", "yes", "no"],
    NewEnableTipGapList=["no", "yes", "no"],
    CombustorType=str,
)

###############################################################################
# Define blade row scope
# ~~~~~~~~~~~~~~~~~~~~~~
# Define the scope of the blade-row analysis.

solver_session.solverworkflow.TWF_BladeRowAnalysisScope(
    ASChildName=str,
    ASSelectComponent="hannover",
    ASRowNumList=["row 1", "row 2", "row 3"],
    OldASIncludeRowList=["yes", "yes", "yes"],
    NewASIncludeRowList=["yes", "yes", "yes"],
)

###############################################################################
# Import Mesh
# ~~~~~~~~~~~
# Import mesh files.

solver_session.solverworkflow.TWF_ImportMesh(
    AddChild=str,
    MeshFilePath=inlet_guide_vane_file,
    MeshFilePath_old="",
    MeshName="IGV.gtm",
    CellZoneNames=[str],
    ListItemLevels=[str],
    ListItemTitles=[str],
    ListOfCellZones=str,
    CellZones=[str],
)

solver_session.solverworkflow.TWF_ImportMesh(
    AddChild=str,
    MeshFilePath=rotor_file,
    MeshFilePath_old="",
    MeshName="R1.gtm",
    CellZoneNames=[str],
    ListItemLevels=[str],
    ListItemTitles=[str],
    ListOfCellZones=str,
    CellZones=[str],
)

solver_session.solverworkflow.TWF_ImportMesh(
    AddChild=str,
    MeshFilePath=stator_file,
    MeshFilePath_old="",
    MeshName="S1.gtm",
    CellZoneNames=[str],
    ListItemLevels=[str],
    ListItemTitles=[str],
    ListOfCellZones=str,
    CellZones=[str],
)

###############################################################################
# Association mesh
# ~~~~~~~~~~~~~~~~
# Associate the mesh.

solver_session.solverworkflow.TWF_AssociateMesh(
    AMChildName=str,
    AMSelectComponentScope=str,
    UseWireframe=True,
    RenameCellZones="Yes, using row names",
    DefaultAMRowNumList=["row 1", "row 2", "row 3"],
    DefaultAMCelZonesList=["", "", ""],
    AMRowNumList=["row 1", "row 2", "row 3"],
    OldAMCellZonesList=[
        "igv-inlet,igv-passage-main",
        "r1-passage-main",
        "s1-passage-main",
    ],
    NewAMCellZonesList=["igv.1,igv.2", "r1", "s1"],
)

###############################################################################
# Define map regions
# ~~~~~~~~~~~~~~~~~~
# Define map regions.

solver_session.solverworkflow.TWF_MapRegionInfo(
    MRChildName="igv.1_region_info",
    MRSelectCellZone="igv.1",
    UseWireframe=True,
    DefaultMRRegionNameList=[
        "hub",
        "shroud",
        "blade",
        "inlet",
        "outlet",
        "symmetry",
        "periodic 1",
        "periodic 2",
        "tip 1",
        "tip 2",
        "interior",
    ],
    DefaultMRFaceZoneList=["", "", "", "", "", "", "", "", "", "", ""],
    MRRegionNameList=[
        "hub",
        "shroud",
        "blade",
        "inlet",
        "outlet",
        "symmetry",
        "periodic 1",
        "periodic 2",
        "tip 1",
        "tip 2",
        "interior",
    ],
    OldMRFaceZoneList=[
        "igv-hub-inblock",
        "igv-shroud-inblock",
        "",
        "igv-inflow-inblock",
        "igv-outflow-inblock",
        "",
        "igv-per1-inblock",
        "igv-per2-inblock",
        "",
        "",
        "default-interior",
    ],
    NewMRFaceZoneList=[
        "igv.1:igv-hub-inblock",
        "igv.1:igv-shroud-inblock",
        "",
        "igv.1:igv-inflow-inblock",
        "igv.1:igv-outflow-inblock",
        "",
        "igv.1:igv-per1-inblock",
        "igv.1:igv-per2-inblock",
        "",
        "",
        "igv.1:default-interior",
    ],
)

solver_session.solverworkflow.TWF_MapRegionInfo(
    MRChildName="igv.2_region_info",
    MRSelectCellZone="igv.2",
    UseWireframe=True,
    DefaultMRRegionNameList=[
        "hub",
        "shroud",
        "blade",
        "inlet",
        "outlet",
        "symmetry",
        "periodic 1",
        "periodic 2",
        "tip 1",
        "tip 2",
        "interior",
    ],
    DefaultMRFaceZoneList=["", "", "", "", "", "", "", "", "", "", ""],
    MRRegionNameList=[
        "hub",
        "shroud",
        "blade",
        "inlet",
        "outlet",
        "symmetry",
        "periodic 1",
        "periodic 2",
        "tip 1",
        "tip 2",
        "interior",
    ],
    OldMRFaceZoneList=[
        "igv-hub-passage",
        "igv-shroud-passage",
        "igv-bld-high-geo-high,igv-bld-high-geo-low,igv-bld-low-geo-high,igv-bld-low-geo-low",
        "igv-inflow-passage",
        "igv-outflow-passage",
        "",
        "igv-per1-passage",
        "igv-per2-passage",
        "",
        "",
        "default-interior:021",
    ],
    NewMRFaceZoneList=[
        "igv.2:igv-hub-passage",
        "igv.2:igv-shroud-passage",
        "igv.2:igv-bld-high-geo-high,igv.2:igv-bld-high-geo-low,igv.2:igv-bld-low-geo-high,igv.2:igv-bld-low-geo-low",
        "igv.2:igv-inflow-passage",
        "igv.2:igv-outflow-passage",
        "",
        "igv.2:igv-per1-passage",
        "igv.2:igv-per2-passage",
        "",
        "",
        "igv.2:default-interior:021",
    ],
)

solver_session.solverworkflow.TWF_MapRegionInfo(
    MRChildName="r1_region_info",
    MRSelectCellZone="r1",
    UseWireframe=True,
    DefaultMRRegionNameList=[
        "hub",
        "shroud",
        "blade",
        "inlet",
        "outlet",
        "symmetry",
        "periodic 1",
        "periodic 2",
        "tip 1",
        "tip 2",
        "interior",
    ],
    DefaultMRFaceZoneList=["", "", "", "", "", "", "", "", "", "", ""],
    MRRegionNameList=[
        "hub",
        "shroud",
        "blade",
        "inlet",
        "outlet",
        "symmetry",
        "periodic 1",
        "periodic 2",
        "tip 1",
        "tip 2",
        "interior",
    ],
    OldMRFaceZoneList=[
        "r1-hub-passage",
        "r1-shroud-passage",
        "r1-bld-high-geo-high,r1-bld-high-geo-low,r1-bld-low-geo-high,r1-bld-low-geo-low"
        "r1-inflow-passage",
        "r1-outflow-passage",
        "",
        "r1-per1-passage",
        "r1-per2-passage",
        "r1-shroud-tip-ggi-side-1-passage",
        "r1-shroud-tip-ggi-side-2-passage",
        "default-interior:1",
    ],
    NewMRFaceZoneList=[
        "r1:r1-hub-passage",
        "r1:r1-shroud-passage",
        "r1:r1-bld-high-geo-high,r1:r1-bld-high-geo-low,r1:r1-bld-low-geo-high,r1:r1-bld-low-geo-low"
        "r1:r1-inflow-passage",
        "r1:r1-outflow-passage",
        "",
        "r1:r1-per1-passage",
        "r1:r1-per2-passage",
        "r1:r1-shroud-tip-ggi-side-1-passage",
        "r1:r1-shroud-tip-ggi-side-2-passage",
        "r1:default-interior:1",
    ],
)

solver_session.solverworkflow.TWF_MapRegionInfo(
    MRChildName="s1_region_info",
    MRSelectCellZone="s1",
    UseWireframe=True,
    DefaultMRRegionNameList=[
        "hub",
        "shroud",
        "blade",
        "inlet",
        "outlet",
        "symmetry",
        "periodic 1",
        "periodic 2",
        "tip 1",
        "tip 2",
        "interior",
    ],
    DefaultMRFaceZoneList=["", "", "", "", "", "", "", "", "", "", ""],
    MRRegionNameList=[
        "hub",
        "shroud",
        "blade",
        "inlet",
        "outlet",
        "symmetry",
        "periodic 1",
        "periodic 2",
        "tip 1",
        "tip 2",
        "interior",
    ],
    OldMRFaceZoneList=[
        "s1-hub-passage",
        "s1-shroud-passage",
        "s1-bld-high-geo-high,s1-bld-high-geo-low,s1-bld-low-geo-high,s1-bld-low-geo-low",
        "s1-inflow-passage",
        "s1-outflow-passage",
        "",
        "s1-per1-passage",
        "s1-per2-passage",
        "",
        "",
        "default-interior_2",
    ],
    NewMRFaceZoneList=[
        "s1:s1-hub-passage",
        "s1:s1-shroud-passage",
        "s1:s1-bld-high-geo-high,s1:s1-bld-high-geo-low,s1:s1-bld-low-geo-high,s1:s1-bld-low-geo-low",
        "s1:s1-inflow-passage",
        "s1:s1-outflow-passage",
        "",
        "s1:s1-per1-passage",
        "s1:s1-per2-passage",
        "",
        "",
        "s1:default-interior_2",
    ],
)

###############################################################################
# Create CFD model
# ~~~~~~~~~~~~~~~~
# Create the CFD model.

solver_session.solverworkflow.TWF_CreateCFDModel(
    CFDMChildName=str,
    CFDMSelectMeshAssociation=str,
    AxisOfRotation="Z",
    DelayCFDModelCreation=False,
    RestrictToFactors=False,
    EstimateNumBlades=False,
    CFDMRowNumList=["igv", "r1", "s1"],
    OldCFDMNumOfBladesList=["", "", ""],
    NewCFDMNumOfBladesList=["26", "23", "30"],
    OldCFDMModelBladesList=["", "", ""],
    NewCFDMModelBladesList=["1", "1", "1"],
    OldCFDMAngleOffset=["", "", ""],
    NewCFDMAngleOffset=["0.0", "0.0", "0.0"],
    OldCFDMBladesPerSectorList=["", "", ""],
    NewCFDMBladesPerSectorList=["1", "1", "1"],
)

###############################################################################
# Define turbo physics
# ~~~~~~~~~~~~~~~~~~
# Define the turbo-related physics conditions.

solver_session.solverworkflow.TWF_TurboPhysics()

###############################################################################
# Turbo regions and zones
# ~~~~~~~~~~~~~~~~~~~~~~~
# Define the turbo-related region and zone boundary conditions.

solver_session.solverworkflow.TWF_TurboRegionsZones()

###############################################################################
# Define turbo-related topology
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Define the turbo-related topology.

solver_session.solverworkflow.TWF_TurboTopology(
    TopologyName="turbo_topology_1",
    UseWireframe=True,
    DefaultTopologyNameList=[
        "hub",
        "casing",
        "theta periodic",
        "theta min",
        "theta max",
        "inlet",
        "outlet",
        "blade",
    ],
    DefaultTopologyZoneList=["", "", "", "", "", "", "", ""],
    TopologyNameList=[
        "hub",
        "casing",
        "theta periodic",
        "theta min",
        "theta max",
        "inlet",
        "outlet",
        "blade",
    ],
    OldTopologyZoneList=[
        "igv-hub-inblock,igv-hub-passage,r1-hub-passage,s1-hub-passage",
        "igv-shroud-inblock,igv-shroud-passage,r1-shroud-passage,s1-shroud-passage",
        "igv-per1-inblock,igv-per2-inblock,igv-per1-passage,igv-per2-passage,r1-per1-passage,r1-per2-passage,s1-per1-passage,s1-per2-passage",
        "",
        "",
        "",
        "",
        "igv-bld-high-geo-high,igv-bld-high-geo-low,igv-bld-low-geo-high,igv-bld-low-geo-low,r1-bld-high-geo-high,r1-bld-high-geo-low,r1-bld-low-geo-high,r1-bld-low-geo-low,r1-bld-shroud-tip,s1-bld-high-geo-high,s1-bld-high-geo-low,s1-bld-low-geo-high,s1-bld-low-geo-low",
    ],
    NewTopologyZoneList=[
        "igv.1:igv-hub-inblock,igv.2:igv-hub-passage,r1:r1-hub-passage,s1:s1-hub-passage",
        "igv.1:igv-shroud-inblock,igv.2:igv-shroud-passage,r1:r1-shroud-passage,s1:s1-shroud-passage",
        "igv.1:igv-per2-inblock,igv.1:igv-per2-passage,periodic_igv.1:igv-per1-inblock_igv.1:igv-per2-inblock,periodic_igv.2:igv.per1-passage_igv.2:igv-per2-passage,periodic_r1:r1-per1-passage_r1:r1-per2-passage,periodic_s1:s1-per1-passage_s1:s1-per2-passage,r1:r1-per2-passage,s1:s1-per2-passage",
        "",
        "",
        "igv.1:igv-inflow-inblock",
        "s1:s1-outflow-passage",
        "igv.2:igv-bld-high-geo-high,igv.2:igv-bld-high-geo-low,igv.2:igv-bld-low-geo-high,igv.2:igv-bld-low-geo-low,r1:r1-bld-high-geo-high,r1:r1-bld-high-geo-low,r1:r1-bld-low-geo-high,r1:r1-bld-low-geo-low,r1:r1-bld-shroud-tip,s1:s1-bld-high-geo-high,s1:s1-bld-high-geo-low,s1:s1-bld-low-geo-high,s1:s1-bld-low-geo-low",
    ],
)

###############################################################################
# Describe turbo surfaces
# ~~~~~~~~~~~~~~~~~~~~~~~
# Define turbo-specific iso-surfaces.

solver_session.solverworkflow.TWF_TurboSurfaces(
    NumIsoSurfaces=3,
    IsoSurfaceNumList=["surface 1", "surface 2", "surface 3"],
    OldIsoSurfaceNameList=["twf_span_1", "twf_span_2", "twf_span_3"],
    NewIsoSurfaceNameList=["twf_span_25", "twf_span_50", "twf_span_75"],
    OldIsoSurfaceValueList=["0.25", "0.5", "0.75"],
    NewIsoSurfaceValueList=["0.25", "0.5", "0.75"],
    SurfacesList=[str],
)

###############################################################################
# Create report definitions and monitors
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Create report definitions and monitors.

solver_session.solverworkflow.TWF_ReportDefMonitors(
    RDIsoSurfaceNumList=["twf_span_25", "twf_span_50", "twf_span_75"],
    OldCreateContourList=["yes", "yes", "yes"],
    NewCreateContourList=["yes", "yes", "yes"],
    TurboContoursList=[str],
)

###############################################################################
# Complete workflow setup
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Complete workflow setup.

solver_session.solverworkflow.TWF_CompleteWorkflowSetup()

#########################################################################
# Close Fluent
# ~~~~~~~~~~~~
# Close Fluent.

solver_session.exit()

###############################################################################
