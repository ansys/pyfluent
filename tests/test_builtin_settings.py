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
    assert Setup(solver=solver) == solver.setup
    assert General(solver=solver) == solver.setup.general
    assert Models(solver=solver) == solver.setup.models
    assert Multiphase(solver=solver) == solver.setup.models.multiphase
    assert Energy(solver=solver) == solver.setup.models.energy
    assert Viscous(solver=solver) == solver.setup.models.viscous
    if solver.get_fluent_version() >= FluentVersion.v232:
        assert Radiation(solver=solver) == solver.setup.models.radiation
    else:
        with pytest.raises(RuntimeError):
            Radiation(solver=solver)
    if solver.get_fluent_version() >= FluentVersion.v232:
        assert Species(solver=solver) == solver.setup.models.species
    else:
        with pytest.raises(RuntimeError):
            Species(solver=solver)
    if solver.get_fluent_version() >= FluentVersion.v231:
        assert DiscretePhase(solver=solver) == solver.setup.models.discrete_phase
    else:
        with pytest.raises(RuntimeError):
            DiscretePhase(solver=solver)
    if solver.get_fluent_version() >= FluentVersion.v231:
        assert (
            Injections(solver=solver) == solver.setup.models.discrete_phase.injections
        )
    else:
        with pytest.raises(RuntimeError):
            Injections(solver=solver)
    if solver.get_fluent_version() >= FluentVersion.v231:
        assert (
            VirtualBladeModel(solver=solver) == solver.setup.models.virtual_blade_model
        )
    else:
        with pytest.raises(RuntimeError):
            VirtualBladeModel(solver=solver)
    if solver.get_fluent_version() >= FluentVersion.v231:
        assert Optics(solver=solver) == solver.setup.models.optics
    else:
        with pytest.raises(RuntimeError):
            Optics(solver=solver)
    if solver.get_fluent_version() >= FluentVersion.v232:
        assert Structure(solver=solver) == solver.setup.models.structure
    else:
        with pytest.raises(RuntimeError):
            Structure(solver=solver)
    if solver.get_fluent_version() >= FluentVersion.v232:
        assert Ablation(solver=solver) == solver.setup.models.ablation
    else:
        with pytest.raises(RuntimeError):
            Ablation(solver=solver)
    if solver.get_fluent_version() >= FluentVersion.v241:
        assert EChemistry(solver=solver) == solver.setup.models.echemistry
    else:
        with pytest.raises(RuntimeError):
            EChemistry(solver=solver)
    if solver.get_fluent_version() >= FluentVersion.v241:
        assert Battery(solver=solver) == solver.setup.models.battery
    else:
        with pytest.raises(RuntimeError):
            Battery(solver=solver)
    if solver.get_fluent_version() >= FluentVersion.v241:
        assert SystemCoupling(solver=solver) == solver.setup.models.system_coupling
    else:
        with pytest.raises(RuntimeError):
            SystemCoupling(solver=solver)
    if solver.get_fluent_version() >= FluentVersion.v241:
        assert Sofc(solver=solver) == solver.setup.models.sofc
    else:
        with pytest.raises(RuntimeError):
            Sofc(solver=solver)
    if solver.get_fluent_version() >= FluentVersion.v242:
        assert Pemfc(solver=solver) == solver.setup.models.pemfc
    else:
        with pytest.raises(RuntimeError):
            Pemfc(solver=solver)
    assert Materials(solver=solver) == solver.setup.materials
    assert FluidMaterials(solver=solver) == solver.setup.materials.fluid
    assert (
        FluidMaterial(solver=solver, name="air") == solver.setup.materials.fluid["air"]
    )
    assert SolidMaterials(solver=solver) == solver.setup.materials.solid
    assert (
        SolidMaterial(solver=solver, name="aluminum")
        == solver.setup.materials.solid["aluminum"]
    )
    assert CellZoneConditions(solver=solver) == solver.setup.cell_zone_conditions
    if solver.get_fluent_version() >= FluentVersion.v231:
        assert (
            CellZoneCondition(solver=solver, name="fluid")
            == solver.setup.cell_zone_conditions["fluid"]
        )
    else:
        with pytest.raises(RuntimeError):
            CellZoneCondition(solver=solver, name="fluid")
    assert FluidCellZones(solver=solver) == solver.setup.cell_zone_conditions.fluid
    assert (
        FluidCellZone(solver=solver, name="fluid")
        == solver.setup.cell_zone_conditions.fluid["fluid"]
    )
    assert BoundaryConditions(solver=solver) == solver.setup.boundary_conditions
    if solver.get_fluent_version() >= FluentVersion.v231:
        assert (
            BoundaryCondition(solver=solver, name="inlet2")
            == solver.setup.boundary_conditions["inlet2"]
        )
    else:
        with pytest.raises(RuntimeError):
            BoundaryCondition(solver=solver, name="inlet2")
    assert (
        VelocityInlets(solver=solver) == solver.setup.boundary_conditions.velocity_inlet
    )
    assert (
        VelocityInlet(solver=solver, name="inlet2")
        == solver.setup.boundary_conditions.velocity_inlet["inlet2"]
    )
    assert (
        InteriorBoundaries(solver=solver) == solver.setup.boundary_conditions.interior
    )
    assert (
        InteriorBoundary(solver=solver, name="interior--fluid")
        == solver.setup.boundary_conditions.interior["interior--fluid"]
    )
    assert (
        PressureOutlets(solver=solver)
        == solver.setup.boundary_conditions.pressure_outlet
    )
    assert (
        PressureOutlet(solver=solver, name="outlet")
        == solver.setup.boundary_conditions.pressure_outlet["outlet"]
    )
    assert WallBoundaries(solver=solver) == solver.setup.boundary_conditions.wall
    assert (
        WallBoundary(solver=solver, name="wall")
        == solver.setup.boundary_conditions.wall["wall"]
    )
    with pytest.raises(TypeError):
        WallBoundary(solver=solver, new_instance_name="wall-1")
    if solver.get_fluent_version() >= FluentVersion.v232:
        assert MeshInterfaces(solver=solver) == solver.setup.mesh_interfaces
    else:
        with pytest.raises(RuntimeError):
            MeshInterfaces(solver=solver)
    if solver.get_fluent_version() >= FluentVersion.v251:
        assert DynamicMesh(solver=solver) == solver.setup.dynamic_mesh
    else:
        with pytest.raises(RuntimeError):
            DynamicMesh(solver=solver)
    assert ReferenceValues(solver=solver) == solver.setup.reference_values
    if solver.get_fluent_version() >= FluentVersion.v232:
        assert ReferenceFrames(solver=solver) == solver.setup.reference_frames
    else:
        with pytest.raises(RuntimeError):
            ReferenceFrames(solver=solver)
    if solver.get_fluent_version() >= FluentVersion.v232:
        # Fluent 25.1 issue
        if solver.get_fluent_version() != FluentVersion.v251:
            assert (
                ReferenceFrame(solver=solver, name="global")
                == solver.setup.reference_frames["global"]
            )
    else:
        with pytest.raises(RuntimeError):
            ReferenceFrame(solver=solver, name="global")
    if solver.get_fluent_version() >= FluentVersion.v232:
        assert NamedExpressions(solver=solver) == solver.setup.named_expressions
    else:
        with pytest.raises(RuntimeError):
            NamedExpressions(solver=solver)
    assert Methods(solver=solver) == solver.solution.methods
    assert Controls(solver=solver) == solver.solution.controls
    assert ReportDefinitions(solver=solver) == solver.solution.report_definitions
    if solver.get_fluent_version() >= FluentVersion.v231:
        assert Monitor(solver=solver) == solver.solution.monitor
        if solver.get_fluent_version() >= FluentVersion.v241:
            assert Residual(solver=solver) == solver.solution.monitor.residual
        else:
            with pytest.raises(RuntimeError):
                Residual(solver=solver)
        assert ReportFiles(solver=solver) == solver.solution.monitor.report_files
        assert (
            ReportFile(solver=solver, new_instance_name="report-file-1")
            == solver.solution.monitor.report_files["report-file-1"]
        )
        assert (
            ReportFile(solver=solver, name="report-file-1")
            == solver.solution.monitor.report_files["report-file-1"]
        )
        if solver.get_fluent_version() >= FluentVersion.v251:
            assert (
                ReportFile(solver=solver)
                == solver.solution.monitor.report_files["report-file-2"]
            )
        assert ReportPlots(solver=solver) == solver.solution.monitor.report_plots
        assert (
            ReportPlot(solver=solver, new_instance_name="report-plot-1")
            == solver.solution.monitor.report_plots["report-plot-1"]
        )
        assert (
            ReportPlot(solver=solver, name="report-plot-1")
            == solver.solution.monitor.report_plots["report-plot-1"]
        )
        if solver.get_fluent_version() >= FluentVersion.v251:
            assert (
                ReportPlot(solver=solver)
                == solver.solution.monitor.report_plots["report-plot-2"]
            )
        assert (
            ConvergenceConditions(solver=solver)
            == solver.solution.monitor.convergence_conditions
        )
    else:
        with pytest.raises(RuntimeError):
            Monitor(solver=solver)
    if solver.get_fluent_version() >= FluentVersion.v231:
        assert CellRegisters(solver=solver) == solver.solution.cell_registers
        assert (
            CellRegister(solver=solver, new_instance_name="cell_register_1")
            == solver.solution.cell_registers["cell_register_1"]
        )
        assert (
            CellRegister(solver=solver, name="cell_register_1")
            == solver.solution.cell_registers["cell_register_1"]
        )
        if solver.get_fluent_version() >= FluentVersion.v251:
            assert (
                CellRegister(solver=solver)
                == solver.solution.cell_registers["cell_register_2"]
            )
    else:
        with pytest.raises(RuntimeError):
            CellRegisters(solver=solver)
    assert Initialization(solver=solver) == solver.solution.initialization
    if solver.get_fluent_version() >= FluentVersion.v231:
        assert (
            CalculationActivity(solver=solver) == solver.solution.calculation_activity
        )
        assert (
            ExecuteCommands(solver=solver)
            == solver.solution.calculation_activity.execute_commands
        )
        if solver.get_fluent_version() >= FluentVersion.v241:
            assert (
                CaseModification(solver=solver)
                == solver.solution.calculation_activity.case_modification
            )
        else:
            with pytest.raises(RuntimeError):
                CaseModification(solver=solver)
    else:
        with pytest.raises(RuntimeError):
            CalculationActivity(solver=solver)
    assert RunCalculation(solver=solver) == solver.solution.run_calculation


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
