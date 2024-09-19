import warnings

import pytest
from pytest import WarningsRecorder

from ansys.fluent.core.examples import download_file
from ansys.fluent.core.solver.flobject import (
    DeprecatedSettingWarning,
    UnstableSettingWarning,
    _Alias,
    _InputFile,
    _OutputFile,
    to_python_name,
)
from ansys.fluent.core.utils.fluent_version import FluentVersion


@pytest.mark.nightly
@pytest.mark.fluent_version(">=23.1")
def test_setup_models_viscous_model_settings(new_solver_session) -> None:
    solver_session = new_solver_session
    case_path = download_file("elbow_source_terms.cas.h5", "pyfluent/mixing_elbow")
    solver_session.file.read(
        file_name=case_path, file_type="case", lightweight_setup=True
    )
    # NOTE: Not sure why initialization is necessary here
    # solver_session.solution.initialization.hybrid_initialize()

    viscous_model = solver_session.setup.models.viscous

    assert viscous_model.model() == "k-epsilon"
    assert "inviscid" in viscous_model.model.get_attr("allowed-values")
    viscous_model.model = "inviscid"

    assert viscous_model.model() == "inviscid"


# Failing for 24.1 but passes for 24.2 and 25.1
@pytest.mark.fluent_version(">=24.2")
def test_wildcard(new_solver_session):
    solver = new_solver_session
    case_path = download_file("elbow_source_terms.cas.h5", "pyfluent/mixing_elbow")
    solver.file.read(file_name=case_path, file_type="case", lightweight_setup=True)
    boundary_conditions = solver.setup.boundary_conditions
    if solver.get_fluent_version() >= FluentVersion.v251:
        assert boundary_conditions.velocity_inlet[
            "inl*"
        ].momentum.velocity_magnitude() == {
            "inlet2": {
                "momentum": {"velocity_magnitude": {"option": "value", "value": 15}}
            },
            "inlet1": {
                "momentum": {"velocity_magnitude": {"option": "value", "value": 5}}
            },
        }
        assert boundary_conditions.velocity_inlet[
            "inl*"
        ].momentum.velocity_magnitude.value() == {
            "inlet2": {"momentum": {"velocity_magnitude": {"value": 15}}},
            "inlet1": {"momentum": {"velocity_magnitude": {"value": 5}}},
        }
        boundary_conditions.velocity_inlet["inl*"].momentum.velocity_magnitude = 10
        assert boundary_conditions.velocity_inlet[
            "inl*"
        ].momentum.velocity_magnitude() == {
            "inlet2": {
                "momentum": {"velocity_magnitude": {"option": "value", "value": 10}}
            },
            "inlet1": {
                "momentum": {"velocity_magnitude": {"option": "value", "value": 10}}
            },
        }
        boundary_conditions.velocity_inlet = boundary_conditions.velocity_inlet[
            "inl*"
        ].momentum.velocity_magnitude()
        assert boundary_conditions.velocity_inlet[
            "inl*"
        ].momentum.velocity_magnitude() == {
            "inlet2": {
                "momentum": {"velocity_magnitude": {"option": "value", "value": 10}}
            },
            "inlet1": {
                "momentum": {"velocity_magnitude": {"option": "value", "value": 10}}
            },
        }
        state = boundary_conditions.velocity_inlet["inl*"]()
        assert state["inlet1"]["momentum"]["velocity_magnitude"]["value"] == 10
        assert state["inlet2"]["momentum"]["velocity_magnitude"]["value"] == 10
        boundary_conditions.velocity_inlet["inl*"] = {
            "momentum": {"velocity_magnitude": {"value": 15}}
        }
        state = boundary_conditions.velocity_inlet["inl*"]()
        assert state["inlet1"]["momentum"]["velocity_magnitude"]["value"] == 15
        assert state["inlet2"]["momentum"]["velocity_magnitude"]["value"] == 15
    else:
        assert boundary_conditions.velocity_inlet["inl*"].momentum.velocity() == {
            "inlet2": {"momentum": {"velocity": {"option": "value", "value": 15}}},
            "inlet1": {"momentum": {"velocity": {"option": "value", "value": 5}}},
        }
        assert boundary_conditions.velocity_inlet["inl*"].momentum.velocity.value() == {
            "inlet2": {"momentum": {"velocity": {"value": 15}}},
            "inlet1": {"momentum": {"velocity": {"value": 5}}},
        }
        boundary_conditions.velocity_inlet["inl*"].momentum.velocity = 10
        assert boundary_conditions.velocity_inlet["inl*"].momentum.velocity() == {
            "inlet2": {"momentum": {"velocity": {"option": "value", "value": 10}}},
            "inlet1": {"momentum": {"velocity": {"option": "value", "value": 10}}},
        }
        boundary_conditions.velocity_inlet = boundary_conditions.velocity_inlet[
            "inl*"
        ].momentum.velocity()
        assert boundary_conditions.velocity_inlet["inl*"].momentum.velocity() == {
            "inlet2": {"momentum": {"velocity": {"option": "value", "value": 10}}},
            "inlet1": {"momentum": {"velocity": {"option": "value", "value": 10}}},
        }
    cell_zone_conditions = solver.setup.cell_zone_conditions
    if solver.get_fluent_version() >= FluentVersion.v242:
        sources = cell_zone_conditions.fluid["*"].sources.terms
        sources_key = "sources"
        terms_key = "terms"
    else:
        sources = cell_zone_conditions.fluid["*"].source_terms.source_terms
        sources_key = terms_key = "source_terms"
    assert sources["*mom*"]() == {
        "fluid": {
            sources_key: {
                terms_key: {
                    "x-momentum": [{"option": "value", "value": 1}],
                    "y-momentum": [{"option": "value", "value": 2}],
                    "z-momentum": [{"option": "value", "value": 3}],
                }
            }
        }
    }
    sources["*mom*"] = [{"option": "value", "value": 2}]
    assert sources["*mom*"]() == {
        "fluid": {
            sources_key: {
                terms_key: {
                    "x-momentum": [{"option": "value", "value": 2}],
                    "y-momentum": [{"option": "value", "value": 2}],
                    "z-momentum": [{"option": "value", "value": 2}],
                }
            }
        }
    }

    with pytest.raises(AttributeError):
        boundary_conditions.velocity_inlet["inl*"].moment


@pytest.mark.fluent_version(">=23.2")
def test_wildcard_fnmatch(new_solver_session):
    solver = new_solver_session
    case_path = download_file("elbow_source_terms.cas.h5", "pyfluent/mixing_elbow")
    solver.file.read_case(file_name=case_path)

    solver.solution.initialization.hybrid_initialize()

    mesh = solver.results.graphics.mesh
    assert mesh.create("mesh-a").name() == "mesh-a"
    mesh.create("mesh-bc")
    if solver.get_fluent_version() >= FluentVersion.v251:
        assert mesh.create(name="mesh-2").name() == "mesh-2"
        assert mesh.create().name() == "mesh-3"
    else:
        assert mesh.create("mesh-2").name() == "mesh-2"
        assert mesh.create("mesh-3").name() == "mesh-3"

    assert sorted(mesh["mesh-*"]()) == sorted(
        ["mesh-1", "mesh-2", "mesh-3", "mesh-a", "mesh-bc"]
    )

    assert list(mesh["mesh-?c"]().keys()) == ["mesh-bc"]

    assert list(mesh["mesh-[2-5]"]().keys()) == ["mesh-2", "mesh-3"]

    assert sorted(mesh["mesh-[!2-5]"]()) == sorted(["mesh-1", "mesh-a"])


@pytest.mark.fluent_version(">=23.2")
def test_wildcard_path_is_iterable(new_solver_session):
    solver = new_solver_session
    case_path = download_file("elbow_source_terms.cas.h5", "pyfluent/mixing_elbow")
    solver.file.read(file_name=case_path, file_type="case", lightweight_setup=True)

    velocity_inlet = solver.setup.boundary_conditions.velocity_inlet
    assert [x for x in velocity_inlet] == ["inlet2", "inlet1"]
    assert [x for x in velocity_inlet["*let*"]] == ["inlet2", "inlet1"]
    assert [x for x in velocity_inlet["*1*"]] == ["inlet1"]

    test_data = []
    for k, v in velocity_inlet.items():
        test_data.append((k, v))

    assert test_data[0][0] == "inlet2"
    assert test_data[0][1].path == r"setup/boundary-conditions/velocity-inlet/inlet2"
    assert test_data[1][0] == "inlet1"
    assert test_data[1][1].path == r"setup/boundary-conditions/velocity-inlet/inlet1"

    test_data = []
    for k, v in velocity_inlet["*let*"].items():
        test_data.append((k, v))

    assert test_data[0][0] == "inlet2"
    assert test_data[0][1].path == r"setup/boundary-conditions/velocity-inlet/inlet2"
    assert test_data[1][0] == "inlet1"
    assert test_data[1][1].path == r"setup/boundary-conditions/velocity-inlet/inlet1"


@pytest.mark.fluent_version(">=23.1")
def test_api_upgrade(new_solver_session, capsys):
    solver = new_solver_session
    case_path = download_file("Static_Mixer_main.cas.h5", "pyfluent/static_mixer")
    solver.tui.file.read_case(case_path)
    "<solver_session>.file.read_case" in capsys.readouterr().out


@pytest.mark.fluent_version(">=24.2")
def test_deprecated_settings_with_custom_aliases(new_solver_session):
    solver = new_solver_session
    if solver.get_fluent_version() >= FluentVersion.v251:
        # https://github.com/ansys/pyfluent/issues/3134
        return
    case_path = download_file("mixing_elbow.cas.h5", "pyfluent/mixing_elbow")
    download_file("mixing_elbow.dat.h5", "pyfluent/mixing_elbow")
    solver.file._setattr("_child_aliases", {"rcd": "read_case_data"})
    with pytest.warns(DeprecatedSettingWarning):
        solver.file.rcd(file_name=case_path)

    solver.setup.boundary_conditions.velocity_inlet.child_object_type._child_aliases[
        "mom"
    ] = "momentum"
    with pytest.warns(DeprecatedSettingWarning):
        solver.setup.boundary_conditions.velocity_inlet["hot-inlet"].mom.velocity = 20
    assert (
        solver.setup.boundary_conditions.velocity_inlet[
            "hot-inlet"
        ].momentum.velocity.value()
        == 20
    )
    with pytest.warns(DeprecatedSettingWarning):
        solver.setup.boundary_conditions.velocity_inlet["cold-inlet"].mom.velocity = 2
    assert (
        solver.setup.boundary_conditions.velocity_inlet[
            "cold-inlet"
        ].momentum.velocity.value()
        == 2
    )

    solver.setup.boundary_conditions.wall["wall-inlet"].thermal.thermal_bc = (
        "Temperature"
    )
    assert (
        len(
            solver.setup.boundary_conditions.wall[
                "wall-inlet"
            ].thermal.temperature._child_aliases
        )
        > 0
    )
    assert (
        solver.setup.boundary_conditions.wall[
            "wall-inlet"
        ].thermal.temperature._child_aliases["constant"]
        == "value"
    )
    with pytest.warns(DeprecatedSettingWarning):
        solver.setup.boundary_conditions.wall[
            "wall-inlet"
        ].thermal.temperature.constant = 400

    assert (
        solver.setup.boundary_conditions.wall["wall-inlet"].thermal.temperature.value()
        == 400
    )
    assert (
        len(
            solver.setup.boundary_conditions.wall[
                "wall-inlet"
            ].thermal.temperature._child_aliases
        )
        > 0
    )
    assert isinstance(
        solver.setup.boundary_conditions.wall[
            "wall-inlet"
        ].thermal.temperature._child_alias_objs["constant"],
        _Alias,
    )
    with pytest.warns(DeprecatedSettingWarning):
        solver.setup.boundary_conditions.wall["wall-inlet"].thermal.t.value = 410

    assert (
        solver.setup.boundary_conditions.wall["wall-inlet"].thermal.temperature.value()
        == 410
    )

    solver.setup.boundary_conditions._setattr("_child_aliases", {"w": "wall"})
    with pytest.warns(DeprecatedSettingWarning):
        solver.setup.boundary_conditions.w["wall-inlet"].thermal.temperature.value = 420

    assert (
        solver.setup.boundary_conditions.wall["wall-inlet"].thermal.temperature.value()
        == 420
    )

    solver.setup._setattr("_child_aliases", {"bc": "boundary_conditions"})
    with pytest.warns(DeprecatedSettingWarning):
        solver.setup.bc.wall["wall-inlet"].thermal.temperature.value = 430

    assert (
        solver.setup.boundary_conditions.wall["wall-inlet"].thermal.temperature.value()
        == 430
    )

    with pytest.warns(DeprecatedSettingWarning):
        solver.setup.boundary_conditions.wall[
            "wall-inlet"
        ].thermal.temperature.constant = 400

    assert (
        solver.setup.boundary_conditions.wall["wall-inlet"].thermal.temperature.value()
        == 400
    )

    solver.results._setattr("_child_aliases", {"gr": "graphics"})
    with pytest.warns(DeprecatedSettingWarning):
        solver.results.gr.contour.create("c1")

    with pytest.warns(DeprecatedSettingWarning):
        solver.results.gr.contour["c1"].field = "pressure"

    assert solver.results.graphics.contour["c1"].field() == "pressure"

    with pytest.warns(DeprecatedSettingWarning):
        del solver.results.gr.contour["c1"]

    assert "c1" not in solver.results.graphics.contour

    solver.setup.boundary_conditions.velocity_inlet[
        "hot-inlet"
    ].momentum.velocity._child_aliases["hd"] = "../../turbulence/hydraulic_diameter"
    with pytest.warns(DeprecatedSettingWarning):
        solver.setup.boundary_conditions.velocity_inlet[
            "hot-inlet"
        ].momentum.velocity.hd = 10
    assert (
        solver.setup.boundary_conditions.velocity_inlet[
            "hot-inlet"
        ].turbulence.hydraulic_diameter()
        == 10
    )

    solver.setup.cell_zone_conditions.fluid["elbow-fluid"] = {"material": "air"}

    solver.setup.boundary_conditions.wall["wall-inlet"] = {
        "thermal": {"q_dot": {"value": 2000000000}, "wall_thickness": {"value": 0.002}}
    }


@pytest.mark.fluent_version(">=25.1")
def test_deprecated_settings_with_settings_api_aliases(new_solver_session):
    solver = new_solver_session
    case_path = download_file("mixing_elbow.cas.h5", "pyfluent/mixing_elbow")
    download_file("mixing_elbow.dat.h5", "pyfluent/mixing_elbow")
    solver.settings.file.read_case_data(file_name=case_path)
    solver.settings.results.surfaces.iso_clip["clip-1"] = {}
    assert solver.settings.results.surfaces.iso_clip["clip-1"].range() == {
        "minimum": 0,
        "maximum": 0,
    }
    solver.settings.results.surfaces.iso_clip["clip-1"] = {
        "min": -0.0001,
        "max": 0.0001,
    }
    assert solver.settings.results.surfaces.iso_clip["clip-1"].range() == {
        "minimum": -0.0001,
        "maximum": 0.0001,
    }


@pytest.mark.fluent_version(">=23.1")
def test_command_return_type(new_solver_session):
    solver = new_solver_session
    version = solver.get_fluent_version()
    case_path = download_file("mixing_elbow.cas.h5", "pyfluent/mixing_elbow")
    download_file("mixing_elbow.dat.h5", "pyfluent/mixing_elbow")
    ret = solver.file.read_case_data(file_name=case_path)
    assert ret is None if version >= FluentVersion.v242 else not None
    solver.solution.report_definitions.surface["surface-1"] = dict(
        surface_names=["cold-inlet"]
    )
    ret = solver.solution.report_definitions.compute(report_defs=["surface-1"])
    assert ret is not None


@pytest.fixture
def warning_record():
    wrec = WarningsRecorder(_ispytest=True)
    with wrec:
        warnings.simplefilter("ignore", ResourceWarning)
        yield wrec


@pytest.mark.skip("https://github.com/ansys/pyfluent/issues/2712")
@pytest.mark.fluent_version(">=24.2")
def test_unstable_settings_warning(new_solver_session, warning_record):
    solver = new_solver_session
    solver.file.export
    assert len(warning_record) == 1
    assert warning_record.pop().category == UnstableSettingWarning
    try:
        solver.file.exp
    except AttributeError:
        pass
    assert len(warning_record) == 0
    solver.file.export
    assert len(warning_record) == 1
    assert warning_record.pop().category == UnstableSettingWarning

    # Issue in running in CI (probably due to -gu mode)
    # case_path = download_file("mixing_elbow.cas.h5", "pyfluent/mixing_elbow")
    # solver.file.read_case_data(file_name=case_path)
    # img_path = "a.png"
    # Path(img_path).unlink(missing_ok=True)
    # solver.results.graphics.picture.save_picture(file_name=img_path)
    # assert len(recwarn) == 0


@pytest.mark.fluent_version(">=24.2")
def test_generated_code_special_cases(new_solver_session):
    solver = new_solver_session
    icing_cls = solver.setup.boundary_conditions._child_classes[
        "velocity_inlet"
    ].child_object_type._child_classes["icing"]
    fensapice_drop_vrh_cls = icing_cls._child_classes["fensapice_drop_vrh"]
    fensapice_drop_vrh_1_cls = icing_cls._child_classes["fensapice_drop_vrh_1"]
    assert fensapice_drop_vrh_cls.fluent_name != fensapice_drop_vrh_1_cls.fluent_name
    assert to_python_name(fensapice_drop_vrh_cls.fluent_name) == to_python_name(
        fensapice_drop_vrh_1_cls.fluent_name
    )
    assert fensapice_drop_vrh_cls.__name__ != fensapice_drop_vrh_1_cls.__name__

    assert (
        solver.file.read_case.file_name.fluent_name
        == solver.file.write_case.file_name.fluent_name
    )
    assert (
        solver.file.read_case.file_name.__class__.__name__
        != solver.file.write_case.file_name.__class__.__name__
    )
    read_file_bases = solver.file.read_case.file_name.__class__.__bases__
    assert _InputFile in read_file_bases
    assert _OutputFile not in read_file_bases
    write_file_bases = solver.file.write_case.file_name.__class__.__bases__
    assert _InputFile not in write_file_bases
    assert _OutputFile in write_file_bases


@pytest.mark.fluent_version(">=25.1")
def test_child_alias_with_parent_path(mixing_elbow_settings_session):
    solver = mixing_elbow_settings_session
    solver.settings.solution.initialization.hybrid_initialize()
    assert (
        solver.settings.setup.models.discrete_phase.numerics.node_based_averaging.kernel._child_aliases
        == {"gaussian_factor": "../gaussian_factor", "option": "../kernel_type"}
    )
    solver.settings.setup.models.discrete_phase.numerics.node_based_averaging.enabled = (
        True
    )
    solver.settings.setup.models.discrete_phase.numerics.node_based_averaging.kernel_type = (
        "inverse-distance"
    )
    solver.settings.setup.models.discrete_phase.numerics.node_based_averaging.kernel = {
        "option": "gaussian",
        "gaussian_factor": 0.5,
    }
    assert (
        solver.settings.setup.models.discrete_phase.numerics.node_based_averaging.kernel_type()
        == "gaussian"
    )
    assert (
        solver.settings.setup.models.discrete_phase.numerics.node_based_averaging.gaussian_factor()
        == 0.5
    )
    solver.settings.setup.models.discrete_phase.numerics.node_based_averaging.kernel.gaussian_factor = (
        0.6
    )
    assert (
        solver.settings.setup.models.discrete_phase.numerics.node_based_averaging.gaussian_factor()
        == 0.6
    )


@pytest.mark.fluent_version(">=25.1")
def test_exit_not_in_settings(new_solver_session):
    solver = new_solver_session

    assert "exit" not in dir(solver.settings)

    with pytest.raises(AttributeError):
        solver.settings.exit()


def test_builtin_settings(static_mixer_case_session):
    from ansys.fluent.core import (
        Ablation,
        Battery,
        BoundaryCondition,
        BoundaryConditions,
        CellZoneCondition,
        CellZoneConditions,
        DiscretePhase,
        DynamicMesh,
        EChemistry,
        Energy,
        FluidCellZone,
        FluidCellZones,
        FluidMaterial,
        FluidMaterials,
        General,
        Injections,
        InteriorBoundaries,
        InteriorBoundary,
        Materials,
        MeshInterfaces,
        Models,
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
