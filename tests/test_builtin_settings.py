from pathlib import Path
import tempfile

import pytest

try:
    from ansys.fluent.core.solver import (
        Ablation,
        Battery,
        BoundaryCondition,
        BoundaryConditions,
        CalculationActivity,
        CaseModification,
        CellRegister,
        CellRegisters,
        CellZoneCondition,
        CellZoneConditions,
        Contour,
        Contours,
        Controls,
        ConvergenceConditions,
        CumulativePlots,
        CustomFieldFunctions,
        CustomVectors,
        DesignPoint,
        DesignPoints,
        DiscretePhase,
        DiscretePhaseHistogram,
        DynamicMesh,
        EChemistry,
        Energy,
        ExecuteCommands,
        ExpressionVolumes,
        FluidCellZone,
        FluidCellZones,
        FluidMaterial,
        FluidMaterials,
        Fluxes,
        General,
        Graphics,
        GroupSurfaces,
        Histogram,
        ImprintSurfaces,
        Initialization,
        Injections,
        InputParameters,
        InteriorBoundaries,
        InteriorBoundary,
        InterpolatedData,
        IsoClips,
        IsoSurfaces,
        LICs,
        LineSurfaces,
        Materials,
        Meshes,
        MeshInterfaces,
        Methods,
        Models,
        Monitor,
        Multiphase,
        NamedExpressions,
        Optics,
        OutputParameters,
        ParametricStudies,
        ParametricStudy,
        ParticleTracks,
        PartitionSurfaces,
        Pathlines,
        Pemfc,
        PlaneSlices,
        PlaneSurface,
        PlaneSurfaces,
        Plots,
        PointSurfaces,
        PressureOutlet,
        PressureOutlets,
        ProfileData,
        QuadricSurfaces,
        Radiation,
        RakeSurfaces,
        ReferenceFrame,
        ReferenceFrames,
        ReferenceValues,
        Report,
        ReportDefinitions,
        ReportFile,
        ReportFiles,
        ReportPlot,
        ReportPlots,
        Residual,
        Results,
        RunCalculation,
        SceneAnimation,
        Scenes,
        Setup,
        SimulationReports,
        Sofc,
        SolidMaterial,
        SolidMaterials,
        Solution,
        Species,
        SphereSlices,
        Structure,
        SurfaceCells,
        SurfaceIntegrals,
        Surfaces,
        SystemCoupling,
        TransformSurfaces,
        Vectors,
        VelocityInlet,
        VelocityInlets,
        VirtualBladeModel,
        Viscous,
        VolumeIntegrals,
        WallBoundaries,
        WallBoundary,
        XYPlots,
        ZoneSurfaces,
    )
except ImportError:
    pass  # for no-codegen testing workflow
import ansys.fluent.core as pyfluent
from ansys.fluent.core.examples import download_file
from ansys.fluent.core.utils.fluent_version import FluentVersion


@pytest.mark.codegen_required
def test_builtin_settings(mixing_elbow_case_data_session):
    solver = mixing_elbow_case_data_session
    fluent_version = solver.get_fluent_version()
    assert Setup(settings_source=solver) == solver.setup
    assert General(settings_source=solver) == solver.setup.general
    assert Models(settings_source=solver) == solver.setup.models
    assert Multiphase(settings_source=solver) == solver.setup.models.multiphase
    assert Energy(settings_source=solver) == solver.setup.models.energy
    assert Viscous(settings_source=solver) == solver.setup.models.viscous
    if fluent_version >= FluentVersion.v232:
        assert Radiation(settings_source=solver) == solver.setup.models.radiation
    else:
        with pytest.raises(RuntimeError):
            Radiation(settings_source=solver)
    if fluent_version >= FluentVersion.v232:
        assert Species(settings_source=solver) == solver.setup.models.species
    else:
        with pytest.raises(RuntimeError):
            Species(settings_source=solver)
    if fluent_version >= FluentVersion.v231:
        assert (
            DiscretePhase(settings_source=solver) == solver.setup.models.discrete_phase
        )
    else:
        with pytest.raises(RuntimeError):
            DiscretePhase(settings_source=solver)
    if fluent_version >= FluentVersion.v231:
        assert (
            Injections(settings_source=solver)
            == solver.setup.models.discrete_phase.injections
        )
    else:
        with pytest.raises(RuntimeError):
            Injections(settings_source=solver)
    if fluent_version >= FluentVersion.v231:
        assert (
            VirtualBladeModel(settings_source=solver)
            == solver.setup.models.virtual_blade_model
        )
    else:
        with pytest.raises(RuntimeError):
            VirtualBladeModel(settings_source=solver)
    if fluent_version >= FluentVersion.v231:
        assert Optics(settings_source=solver) == solver.setup.models.optics
    else:
        with pytest.raises(RuntimeError):
            Optics(settings_source=solver)
    if fluent_version >= FluentVersion.v232:
        assert Structure(settings_source=solver) == solver.setup.models.structure
    else:
        with pytest.raises(RuntimeError):
            Structure(settings_source=solver)
    if fluent_version >= FluentVersion.v232:
        assert Ablation(settings_source=solver) == solver.setup.models.ablation
    else:
        with pytest.raises(RuntimeError):
            Ablation(settings_source=solver)
    if fluent_version >= FluentVersion.v241:
        assert EChemistry(settings_source=solver) == solver.setup.models.echemistry
    else:
        with pytest.raises(RuntimeError):
            EChemistry(settings_source=solver)
    if fluent_version >= FluentVersion.v241:
        assert Battery(settings_source=solver) == solver.setup.models.battery
    else:
        with pytest.raises(RuntimeError):
            Battery(settings_source=solver)
    if fluent_version >= FluentVersion.v241:
        assert (
            SystemCoupling(settings_source=solver)
            == solver.setup.models.system_coupling
        )
    else:
        with pytest.raises(RuntimeError):
            SystemCoupling(settings_source=solver)
    if fluent_version >= FluentVersion.v241:
        assert Sofc(settings_source=solver) == solver.setup.models.sofc
    else:
        with pytest.raises(RuntimeError):
            Sofc(settings_source=solver)
    if fluent_version >= FluentVersion.v242:
        assert Pemfc(settings_source=solver) == solver.setup.models.pemfc
    else:
        with pytest.raises(RuntimeError):
            Pemfc(settings_source=solver)
    assert Materials(settings_source=solver) == solver.setup.materials
    assert FluidMaterials(settings_source=solver) == solver.setup.materials.fluid
    assert (
        FluidMaterial(settings_source=solver, name="air")
        == solver.setup.materials.fluid["air"]
    )
    assert SolidMaterials(settings_source=solver) == solver.setup.materials.solid
    assert (
        SolidMaterial(settings_source=solver, name="aluminum")
        == solver.setup.materials.solid["aluminum"]
    )
    assert (
        CellZoneConditions(settings_source=solver) == solver.setup.cell_zone_conditions
    )
    if fluent_version >= FluentVersion.v231:
        assert (
            CellZoneCondition(settings_source=solver, name="elbow-fluid")
            == solver.setup.cell_zone_conditions["elbow-fluid"]
        )
    else:
        with pytest.raises(RuntimeError):
            CellZoneCondition(settings_source=solver, name="elbow-fluid")
    assert (
        FluidCellZones(settings_source=solver)
        == solver.setup.cell_zone_conditions.fluid
    )
    assert (
        FluidCellZone(settings_source=solver, name="elbow-fluid")
        == solver.setup.cell_zone_conditions.fluid["elbow-fluid"]
    )
    assert (
        BoundaryConditions(settings_source=solver) == solver.setup.boundary_conditions
    )
    if fluent_version >= FluentVersion.v231:
        assert (
            BoundaryCondition(settings_source=solver, name="cold-inlet")
            == solver.setup.boundary_conditions["cold-inlet"]
        )
    else:
        with pytest.raises(RuntimeError):
            BoundaryCondition(settings_source=solver, name="cold-inlet")
    with pytest.raises(TypeError):
        BoundaryCondition(settings_source=solver, new_instance_name="bc-1")
    assert (
        VelocityInlets(settings_source=solver)
        == solver.setup.boundary_conditions.velocity_inlet
    )
    assert (
        VelocityInlet(settings_source=solver, name="cold-inlet")
        == solver.setup.boundary_conditions.velocity_inlet["cold-inlet"]
    )
    assert (
        InteriorBoundaries(settings_source=solver)
        == solver.setup.boundary_conditions.interior
    )
    assert (
        InteriorBoundary(settings_source=solver, name="interior--elbow-fluid")
        == solver.setup.boundary_conditions.interior["interior--elbow-fluid"]
    )
    assert (
        PressureOutlets(settings_source=solver)
        == solver.setup.boundary_conditions.pressure_outlet
    )
    assert (
        PressureOutlet(settings_source=solver, name="outlet")
        == solver.setup.boundary_conditions.pressure_outlet["outlet"]
    )
    assert (
        WallBoundaries(settings_source=solver) == solver.setup.boundary_conditions.wall
    )
    assert (
        WallBoundary(settings_source=solver, name="wall-elbow")
        == solver.setup.boundary_conditions.wall["wall-elbow"]
    )
    if fluent_version >= FluentVersion.v231 and fluent_version < FluentVersion.v251:
        with pytest.raises(AttributeError):
            WallBoundary(settings_source=solver, new_instance_name="wall-1")
    if fluent_version >= FluentVersion.v232:
        assert MeshInterfaces(settings_source=solver) == solver.setup.mesh_interfaces
    else:
        with pytest.raises(RuntimeError):
            MeshInterfaces(settings_source=solver)
    if fluent_version >= FluentVersion.v251:
        assert DynamicMesh(settings_source=solver) == solver.setup.dynamic_mesh
    else:
        with pytest.raises(RuntimeError):
            DynamicMesh(settings_source=solver)
    assert ReferenceValues(settings_source=solver) == solver.setup.reference_values
    if fluent_version >= FluentVersion.v232:
        assert ReferenceFrames(settings_source=solver) == solver.setup.reference_frames
    else:
        with pytest.raises(RuntimeError):
            ReferenceFrames(settings_source=solver)
    if fluent_version >= FluentVersion.v232:
        # Fluent 25.1 issue
        if fluent_version != FluentVersion.v251:
            assert (
                ReferenceFrame(settings_source=solver, name="global")
                == solver.setup.reference_frames["global"]
            )
    else:
        with pytest.raises(RuntimeError):
            ReferenceFrame(settings_source=solver, name="global")
    if fluent_version >= FluentVersion.v232:
        assert (
            NamedExpressions(settings_source=solver) == solver.setup.named_expressions
        )
    else:
        with pytest.raises(RuntimeError):
            NamedExpressions(settings_source=solver)
    assert Methods(settings_source=solver) == solver.solution.methods
    assert Controls(settings_source=solver) == solver.solution.controls
    assert (
        ReportDefinitions(settings_source=solver) == solver.solution.report_definitions
    )
    if fluent_version >= FluentVersion.v231:
        assert Monitor(settings_source=solver) == solver.solution.monitor
        if fluent_version >= FluentVersion.v241:
            assert Residual(settings_source=solver) == solver.solution.monitor.residual
        else:
            with pytest.raises(RuntimeError):
                Residual(settings_source=solver)
        assert (
            ReportFiles(settings_source=solver) == solver.solution.monitor.report_files
        )
        assert (
            ReportFile(settings_source=solver, new_instance_name="report-file-1")
            == solver.solution.monitor.report_files["report-file-1"]
        )
        assert (
            ReportFile(settings_source=solver, name="report-file-1")
            == solver.solution.monitor.report_files["report-file-1"]
        )
        if fluent_version >= FluentVersion.v251:
            assert (
                ReportFile(settings_source=solver)
                == solver.solution.monitor.report_files["report-file-2"]
            )
        assert (
            ReportPlots(settings_source=solver) == solver.solution.monitor.report_plots
        )
        assert (
            ReportPlot(settings_source=solver, new_instance_name="report-plot-1")
            == solver.solution.monitor.report_plots["report-plot-1"]
        )
        assert (
            ReportPlot(settings_source=solver, name="report-plot-1")
            == solver.solution.monitor.report_plots["report-plot-1"]
        )
        if fluent_version >= FluentVersion.v251:
            assert (
                ReportPlot(settings_source=solver)
                == solver.solution.monitor.report_plots["report-plot-2"]
            )
        assert (
            ConvergenceConditions(settings_source=solver)
            == solver.solution.monitor.convergence_conditions
        )
    else:
        with pytest.raises(RuntimeError):
            Monitor(settings_source=solver)
    if fluent_version >= FluentVersion.v231:
        assert CellRegisters(settings_source=solver) == solver.solution.cell_registers
        assert (
            CellRegister(settings_source=solver, new_instance_name="cell_register_1")
            == solver.solution.cell_registers["cell_register_1"]
        )
        assert (
            CellRegister(settings_source=solver, name="cell_register_1")
            == solver.solution.cell_registers["cell_register_1"]
        )
        if fluent_version >= FluentVersion.v251:
            assert (
                CellRegister(settings_source=solver)
                == solver.solution.cell_registers["cell_register_2"]
            )
    else:
        with pytest.raises(RuntimeError):
            CellRegisters(settings_source=solver)
    assert Initialization(settings_source=solver) == solver.solution.initialization
    if fluent_version >= FluentVersion.v231:
        assert (
            CalculationActivity(settings_source=solver)
            == solver.solution.calculation_activity
        )
        assert (
            ExecuteCommands(settings_source=solver)
            == solver.solution.calculation_activity.execute_commands
        )
        if fluent_version >= FluentVersion.v241:
            assert (
                CaseModification(settings_source=solver)
                == solver.solution.calculation_activity.case_modification
            )
        else:
            with pytest.raises(RuntimeError):
                CaseModification(settings_source=solver)
    else:
        with pytest.raises(RuntimeError):
            CalculationActivity(settings_source=solver)
    assert RunCalculation(settings_source=solver) == solver.solution.run_calculation
    assert Solution(settings_source=solver) == solver.solution
    assert Results(settings_source=solver) == solver.results
    assert Surfaces(settings_source=solver) == solver.results.surfaces
    if fluent_version >= FluentVersion.v232:
        assert (
            PointSurfaces(settings_source=solver)
            == solver.results.surfaces.point_surface
        )
        assert (
            LineSurfaces(settings_source=solver) == solver.results.surfaces.line_surface
        )
        assert (
            RakeSurfaces(settings_source=solver) == solver.results.surfaces.rake_surface
        )
        assert (
            IsoSurfaces(settings_source=solver) == solver.results.surfaces.iso_surface
        )
    else:
        with pytest.raises(RuntimeError):
            PointSurfaces(settings_source=solver)
        with pytest.raises(RuntimeError):
            LineSurfaces(settings_source=solver)
        with pytest.raises(RuntimeError):
            RakeSurfaces(settings_source=solver)
        with pytest.raises(RuntimeError):
            IsoSurfaces(settings_source=solver)
    assert (
        PlaneSurfaces(settings_source=solver) == solver.results.surfaces.plane_surface
    )
    assert (
        PlaneSurface(settings_source=solver, new_instance_name="plane-1")
        == solver.results.surfaces.plane_surface["plane-1"]
    )
    assert (
        PlaneSurface(settings_source=solver, name="plane-1")
        == solver.results.surfaces.plane_surface["plane-1"]
    )
    if fluent_version >= FluentVersion.v241:
        assert IsoClips(settings_source=solver) == solver.results.surfaces.iso_clip
    else:
        with pytest.raises(RuntimeError):
            IsoClips(settings_source=solver)
    if fluent_version >= FluentVersion.v241:
        assert (
            ZoneSurfaces(settings_source=solver) == solver.results.surfaces.zone_surface
        )
        assert (
            PartitionSurfaces(settings_source=solver)
            == solver.results.surfaces.partition_surface
        )
        assert (
            TransformSurfaces(settings_source=solver)
            == solver.results.surfaces.transform_surface
        )
        assert (
            ImprintSurfaces(settings_source=solver)
            == solver.results.surfaces.imprint_surface
        )
        assert (
            PlaneSlices(settings_source=solver) == solver.results.surfaces.plane_slice
        )
        assert (
            SphereSlices(settings_source=solver) == solver.results.surfaces.sphere_slice
        )
        assert (
            QuadricSurfaces(settings_source=solver)
            == solver.results.surfaces.quadric_surface
        )
        assert (
            SurfaceCells(settings_source=solver)
            == solver.results.surfaces.surface_cells
        )
    else:
        with pytest.raises(RuntimeError):
            ZoneSurfaces(settings_source=solver)
        with pytest.raises(RuntimeError):
            PartitionSurfaces(settings_source=solver)
        with pytest.raises(RuntimeError):
            TransformSurfaces(settings_source=solver)
        with pytest.raises(RuntimeError):
            ImprintSurfaces(settings_source=solver)
        with pytest.raises(RuntimeError):
            PlaneSlices(settings_source=solver)
        with pytest.raises(RuntimeError):
            SphereSlices(settings_source=solver)
        with pytest.raises(RuntimeError):
            QuadricSurfaces(settings_source=solver)
        with pytest.raises(RuntimeError):
            SurfaceCells(settings_source=solver)
    if fluent_version >= FluentVersion.v251:
        assert (
            ExpressionVolumes(settings_source=solver)
            == solver.results.surfaces.expression_volume
        )
        assert (
            GroupSurfaces(settings_source=solver)
            == solver.results.surfaces.group_surface
        )
    else:
        with pytest.raises(RuntimeError):
            ExpressionVolumes(settings_source=solver)
        with pytest.raises(RuntimeError):
            GroupSurfaces(settings_source=solver)
    assert Graphics(settings_source=solver) == solver.results.graphics
    assert Meshes(settings_source=solver) == solver.results.graphics.mesh
    assert Contours(settings_source=solver) == solver.results.graphics.contour
    assert (
        Contour(settings_source=solver, new_instance_name="contour-1")
        == solver.results.graphics.contour["contour-1"]
    )
    assert (
        Contour(settings_source=solver, name="contour-1")
        == solver.results.graphics.contour["contour-1"]
    )
    assert Vectors(settings_source=solver) == solver.results.graphics.vector
    assert LICs(settings_source=solver) == solver.results.graphics.lic
    if fluent_version >= FluentVersion.v231:
        assert Pathlines(settings_source=solver) == solver.results.graphics.pathline
        assert (
            ParticleTracks(settings_source=solver)
            == solver.results.graphics.particle_track
        )
        assert Plots(settings_source=solver) == solver.results.plot
        assert XYPlots(settings_source=solver) == solver.results.plot.xy_plot
    else:
        with pytest.raises(RuntimeError):
            Pathlines(settings_source=solver)
        with pytest.raises(RuntimeError):
            ParticleTracks(settings_source=solver)
        with pytest.raises(RuntimeError):
            Plots(settings_source=solver)
        with pytest.raises(RuntimeError):
            XYPlots(settings_source=solver)
    if fluent_version >= FluentVersion.v241:
        assert Histogram(settings_source=solver) == solver.results.plot.histogram
        assert (
            CumulativePlots(settings_source=solver)
            == solver.results.plot.cumulative_plot
        )
    else:
        with pytest.raises(RuntimeError):
            Histogram(settings_source=solver)
        with pytest.raises(RuntimeError):
            CumulativePlots(settings_source=solver)
    if fluent_version >= FluentVersion.v242:
        assert ProfileData(settings_source=solver) == solver.results.plot.profile_data
        assert (
            InterpolatedData(settings_source=solver)
            == solver.results.plot.interpolated_data
        )
    else:
        with pytest.raises(RuntimeError):
            ProfileData(settings_source=solver)
        with pytest.raises(RuntimeError):
            InterpolatedData(settings_source=solver)
    if fluent_version >= FluentVersion.v231:
        assert Scenes(settings_source=solver) == solver.results.scene
    else:
        with pytest.raises(RuntimeError):
            Scenes(settings_source=solver)
    if fluent_version >= FluentVersion.v241:
        assert (
            SceneAnimation(settings_source=solver)
            == solver.results.animations.scene_animation
        )
    else:
        with pytest.raises(RuntimeError):
            SceneAnimation(settings_source=solver)
    if fluent_version >= FluentVersion.v231:
        assert Report(settings_source=solver) == solver.results.report
        assert (
            DiscretePhaseHistogram(settings_source=solver)
            == solver.results.report.discrete_phase.histogram
        )
        assert Fluxes(settings_source=solver) == solver.results.report.fluxes
        assert (
            SurfaceIntegrals(settings_source=solver)
            == solver.results.report.surface_integrals
        )
        assert (
            VolumeIntegrals(settings_source=solver)
            == solver.results.report.volume_integrals
        )
        assert (
            SimulationReports(settings_source=solver)
            == solver.results.report.simulation_reports
        )
    else:
        with pytest.raises(RuntimeError):
            Report(settings_source=solver)
        with pytest.raises(RuntimeError):
            DiscretePhaseHistogram(settings_source=solver)
        with pytest.raises(RuntimeError):
            Fluxes(settings_source=solver)
        with pytest.raises(RuntimeError):
            SurfaceIntegrals(settings_source=solver)
        with pytest.raises(RuntimeError):
            VolumeIntegrals(settings_source=solver)
        with pytest.raises(RuntimeError):
            SimulationReports(settings_source=solver)
    if fluent_version >= FluentVersion.v241:
        assert (
            InputParameters(settings_source=solver)
            == solver.parameters.input_parameters
        )
        assert (
            OutputParameters(settings_source=solver)
            == solver.parameters.output_parameters
        )
    else:
        with pytest.raises(RuntimeError):
            InputParameters(settings_source=solver)
        with pytest.raises(RuntimeError):
            OutputParameters(settings_source=solver)
    if fluent_version >= FluentVersion.v251:
        assert (
            CustomFieldFunctions(settings_source=solver)
            == solver.results.custom_field_functions
        )
    else:
        with pytest.raises(RuntimeError):
            CustomFieldFunctions(settings_source=solver)
    if fluent_version >= FluentVersion.v241:
        assert CustomVectors(settings_source=solver) == solver.results.custom_vectors
    else:
        with pytest.raises(RuntimeError):
            CustomVectors(settings_source=solver)
    tmp_save_path = tempfile.mkdtemp(dir=pyfluent.EXAMPLES_PATH)
    project_file = Path(tmp_save_path) / "mixing_elbow_param.flprj"
    solver.settings.parametric_studies.initialize(project_filename=str(project_file))
    assert ParametricStudies(settings_source=solver) == solver.parametric_studies
    assert (
        ParametricStudy(settings_source=solver, name="mixing_elbow-Solve")
        == solver.parametric_studies["mixing_elbow-Solve"]
    )
    assert (
        DesignPoints(settings_source=solver, parametric_studies="mixing_elbow-Solve")
        == solver.parametric_studies["mixing_elbow-Solve"].design_points
    )
    assert (
        DesignPoint(
            settings_source=solver,
            parametric_studies="mixing_elbow-Solve",
            name="Base DP",
        )
        == solver.parametric_studies["mixing_elbow-Solve"].design_points["Base DP"]
    )


@pytest.mark.codegen_required
@pytest.mark.fluent_version(">=23.2")
def test_builtin_singleton_setting_assign_session(
    new_meshing_session, new_solver_session
):
    meshing = new_meshing_session
    solver = new_solver_session

    models = Models()
    assert isinstance(models, Models)
    with pytest.raises(TypeError):
        models.settings_source = meshing
    models.settings_source = solver
    assert models.settings_source == solver.settings
    assert not isinstance(models, Models)
    assert models.path == "setup/models"
    assert not models.is_active()
    case_name = download_file("Static_Mixer_main.cas.h5", "pyfluent/static_mixer")
    solver.file.read(
        file_type="case",
        file_name=case_name,
        lightweight_setup=True,
    )
    assert models.is_active()
    assert models == solver.setup.models
    # TODO: Ideally an AttributeError should be raised here from flobject.py
    with pytest.raises(RuntimeError):  # re-assignment is not allowed
        models.settings_source = solver

    models = Models()
    assert isinstance(models, Models)
    models.settings_source = solver.settings
    assert models == solver.setup.models
    assert models.settings_source == solver.settings


@pytest.mark.codegen_required
@pytest.mark.fluent_version(">=23.2")
def test_builtin_non_creatable_named_object_setting_assign_session(
    new_meshing_session, static_mixer_case_session
):
    meshing = new_meshing_session
    solver = static_mixer_case_session

    inlet = BoundaryCondition(name="inlet1")
    assert isinstance(inlet, BoundaryCondition)
    with pytest.raises(TypeError):
        inlet.settings_source = meshing
    inlet.settings_source = solver
    assert inlet == solver.settings.setup.boundary_conditions["inlet1"]
    assert inlet.settings_source == solver.settings
    # TODO: Ideally an AttributeError should be raised here from flobject.py
    with pytest.raises(RuntimeError):  # re-assignment is not allowed
        inlet.settings_source = solver

    inlet = BoundaryCondition(name="inlet1")
    assert isinstance(inlet, BoundaryCondition)
    inlet.settings_source = solver.settings
    assert inlet == solver.settings.setup.boundary_conditions["inlet1"]
    assert inlet.settings_source == solver.settings


@pytest.mark.codegen_required
@pytest.mark.fluent_version(">=23.2")
def test_builtin_creatable_named_object_setting_assign_session(
    new_meshing_session, static_mixer_case_session
):
    meshing = new_meshing_session
    solver = static_mixer_case_session

    report_file = ReportFile(new_instance_name="report-file-1")
    assert isinstance(report_file, ReportFile)
    with pytest.raises(TypeError):
        report_file.settings_source = meshing
    report_file.settings_source = solver
    assert report_file == solver.solution.monitor.report_files["report-file-1"]
    assert report_file.settings_source == solver.settings
    # TODO: Ideally an AttributeError should be raised here from flobject.py
    with pytest.raises(RuntimeError):  # re-assignment is not allowed
        report_file.settings_source = solver

    report_file = ReportFile(name="report-file-1")
    assert isinstance(report_file, ReportFile)
    report_file.settings_source = solver
    assert report_file == solver.solution.monitor.report_files["report-file-1"]
    assert report_file.settings_source == solver.settings

    report_file = ReportFile(name="report-file-1")
    assert isinstance(report_file, ReportFile)
    report_file.settings_source = solver.settings
    assert report_file == solver.solution.monitor.report_files["report-file-1"]
    assert report_file.settings_source == solver.settings

    if solver.get_fluent_version() >= FluentVersion.v251:
        report_file = ReportFile()
        assert isinstance(report_file, ReportFile)
        report_file.settings_source = solver
        assert report_file == solver.solution.monitor.report_files["report-file-2"]
        assert report_file.settings_source == solver.settings
