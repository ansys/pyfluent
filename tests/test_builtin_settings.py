import pytest

from ansys.fluent.core import (
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
    Controls,
    ConvergenceConditions,
    DiscretePhase,
    DynamicMesh,
    EChemistry,
    Energy,
    ExecuteCommands,
    FluidCellZone,
    FluidCellZones,
    FluidMaterial,
    FluidMaterials,
    General,
    Initialization,
    Injections,
    InteriorBoundaries,
    InteriorBoundary,
    Materials,
    MeshInterfaces,
    Methods,
    Models,
    Monitor,
    Multiphase,
    NamedExpressions,
    Optics,
    Pemfc,
    PressureOutlet,
    PressureOutlets,
    Radiation,
    ReferenceFrame,
    ReferenceFrames,
    ReferenceValues,
    ReportDefinitions,
    ReportFile,
    ReportFiles,
    ReportPlot,
    ReportPlots,
    Residual,
    RunCalculation,
    Setup,
    Sofc,
    SolidMaterial,
    SolidMaterials,
    Species,
    Structure,
    SystemCoupling,
    VelocityInlet,
    VelocityInlets,
    VirtualBladeModel,
    Viscous,
    WallBoundaries,
    WallBoundary,
)
from ansys.fluent.core.examples import download_file
from ansys.fluent.core.utils.fluent_version import FluentVersion


def test_builtin_settings(static_mixer_case_session):
    solver = static_mixer_case_session
    assert Setup(settings_source=solver) == solver.setup
    assert General(settings_source=solver) == solver.setup.general
    assert Models(settings_source=solver) == solver.setup.models
    assert Multiphase(settings_source=solver) == solver.setup.models.multiphase
    assert Energy(settings_source=solver) == solver.setup.models.energy
    assert Viscous(settings_source=solver) == solver.setup.models.viscous
    if solver.get_fluent_version() >= FluentVersion.v232:
        assert Radiation(settings_source=solver) == solver.setup.models.radiation
    else:
        with pytest.raises(RuntimeError):
            Radiation(settings_source=solver)
    if solver.get_fluent_version() >= FluentVersion.v232:
        assert Species(settings_source=solver) == solver.setup.models.species
    else:
        with pytest.raises(RuntimeError):
            Species(settings_source=solver)
    if solver.get_fluent_version() >= FluentVersion.v231:
        assert (
            DiscretePhase(settings_source=solver) == solver.setup.models.discrete_phase
        )
    else:
        with pytest.raises(RuntimeError):
            DiscretePhase(settings_source=solver)
    if solver.get_fluent_version() >= FluentVersion.v231:
        assert (
            Injections(settings_source=solver)
            == solver.setup.models.discrete_phase.injections
        )
    else:
        with pytest.raises(RuntimeError):
            Injections(settings_source=solver)
    if solver.get_fluent_version() >= FluentVersion.v231:
        assert (
            VirtualBladeModel(settings_source=solver)
            == solver.setup.models.virtual_blade_model
        )
    else:
        with pytest.raises(RuntimeError):
            VirtualBladeModel(settings_source=solver)
    if solver.get_fluent_version() >= FluentVersion.v231:
        assert Optics(settings_source=solver) == solver.setup.models.optics
    else:
        with pytest.raises(RuntimeError):
            Optics(settings_source=solver)
    if solver.get_fluent_version() >= FluentVersion.v232:
        assert Structure(settings_source=solver) == solver.setup.models.structure
    else:
        with pytest.raises(RuntimeError):
            Structure(settings_source=solver)
    if solver.get_fluent_version() >= FluentVersion.v232:
        assert Ablation(settings_source=solver) == solver.setup.models.ablation
    else:
        with pytest.raises(RuntimeError):
            Ablation(settings_source=solver)
    if solver.get_fluent_version() >= FluentVersion.v241:
        assert EChemistry(settings_source=solver) == solver.setup.models.echemistry
    else:
        with pytest.raises(RuntimeError):
            EChemistry(settings_source=solver)
    if solver.get_fluent_version() >= FluentVersion.v241:
        assert Battery(settings_source=solver) == solver.setup.models.battery
    else:
        with pytest.raises(RuntimeError):
            Battery(settings_source=solver)
    if solver.get_fluent_version() >= FluentVersion.v241:
        assert (
            SystemCoupling(settings_source=solver)
            == solver.setup.models.system_coupling
        )
    else:
        with pytest.raises(RuntimeError):
            SystemCoupling(settings_source=solver)
    if solver.get_fluent_version() >= FluentVersion.v241:
        assert Sofc(settings_source=solver) == solver.setup.models.sofc
    else:
        with pytest.raises(RuntimeError):
            Sofc(settings_source=solver)
    if solver.get_fluent_version() >= FluentVersion.v242:
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
    if solver.get_fluent_version() >= FluentVersion.v231:
        assert (
            CellZoneCondition(settings_source=solver, name="fluid")
            == solver.setup.cell_zone_conditions["fluid"]
        )
    else:
        with pytest.raises(RuntimeError):
            CellZoneCondition(settings_source=solver, name="fluid")
    assert (
        FluidCellZones(settings_source=solver)
        == solver.setup.cell_zone_conditions.fluid
    )
    assert (
        FluidCellZone(settings_source=solver, name="fluid")
        == solver.setup.cell_zone_conditions.fluid["fluid"]
    )
    assert (
        BoundaryConditions(settings_source=solver) == solver.setup.boundary_conditions
    )
    if solver.get_fluent_version() >= FluentVersion.v231:
        assert (
            BoundaryCondition(settings_source=solver, name="inlet2")
            == solver.setup.boundary_conditions["inlet2"]
        )
    else:
        with pytest.raises(RuntimeError):
            BoundaryCondition(settings_source=solver, name="inlet2")
    assert (
        VelocityInlets(settings_source=solver)
        == solver.setup.boundary_conditions.velocity_inlet
    )
    assert (
        VelocityInlet(settings_source=solver, name="inlet2")
        == solver.setup.boundary_conditions.velocity_inlet["inlet2"]
    )
    assert (
        InteriorBoundaries(settings_source=solver)
        == solver.setup.boundary_conditions.interior
    )
    assert (
        InteriorBoundary(settings_source=solver, name="interior--fluid")
        == solver.setup.boundary_conditions.interior["interior--fluid"]
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
        WallBoundary(settings_source=solver, name="wall")
        == solver.setup.boundary_conditions.wall["wall"]
    )
    with pytest.raises(TypeError):
        WallBoundary(settings_source=solver, new_instance_name="wall-1")
    if solver.get_fluent_version() >= FluentVersion.v232:
        assert MeshInterfaces(settings_source=solver) == solver.setup.mesh_interfaces
    else:
        with pytest.raises(RuntimeError):
            MeshInterfaces(settings_source=solver)
    if solver.get_fluent_version() >= FluentVersion.v251:
        assert DynamicMesh(settings_source=solver) == solver.setup.dynamic_mesh
    else:
        with pytest.raises(RuntimeError):
            DynamicMesh(settings_source=solver)
    assert ReferenceValues(settings_source=solver) == solver.setup.reference_values
    if solver.get_fluent_version() >= FluentVersion.v232:
        assert ReferenceFrames(settings_source=solver) == solver.setup.reference_frames
    else:
        with pytest.raises(RuntimeError):
            ReferenceFrames(settings_source=solver)
    if solver.get_fluent_version() >= FluentVersion.v232:
        # Fluent 25.1 issue
        if solver.get_fluent_version() != FluentVersion.v251:
            assert (
                ReferenceFrame(settings_source=solver, name="global")
                == solver.setup.reference_frames["global"]
            )
    else:
        with pytest.raises(RuntimeError):
            ReferenceFrame(settings_source=solver, name="global")
    if solver.get_fluent_version() >= FluentVersion.v232:
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
    if solver.get_fluent_version() >= FluentVersion.v231:
        assert Monitor(settings_source=solver) == solver.solution.monitor
        if solver.get_fluent_version() >= FluentVersion.v241:
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
        if solver.get_fluent_version() >= FluentVersion.v251:
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
        if solver.get_fluent_version() >= FluentVersion.v251:
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
    if solver.get_fluent_version() >= FluentVersion.v231:
        assert CellRegisters(settings_source=solver) == solver.solution.cell_registers
        assert (
            CellRegister(settings_source=solver, new_instance_name="cell_register_1")
            == solver.solution.cell_registers["cell_register_1"]
        )
        assert (
            CellRegister(settings_source=solver, name="cell_register_1")
            == solver.solution.cell_registers["cell_register_1"]
        )
        if solver.get_fluent_version() >= FluentVersion.v251:
            assert (
                CellRegister(settings_source=solver)
                == solver.solution.cell_registers["cell_register_2"]
            )
    else:
        with pytest.raises(RuntimeError):
            CellRegisters(settings_source=solver)
    assert Initialization(settings_source=solver) == solver.solution.initialization
    if solver.get_fluent_version() >= FluentVersion.v231:
        assert (
            CalculationActivity(settings_source=solver)
            == solver.solution.calculation_activity
        )
        assert (
            ExecuteCommands(settings_source=solver)
            == solver.solution.calculation_activity.execute_commands
        )
        if solver.get_fluent_version() >= FluentVersion.v241:
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
