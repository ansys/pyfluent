"""Unit tests for flobject module."""

from collections.abc import MutableMapping
import io
import weakref

import pytest
from test_utils import count_key_recursive

from ansys.fluent.core.examples import download_file
from ansys.fluent.core.solver import flobject
from ansys.fluent.core.solver.flobject import (
    InactiveObjectError,
    _gethash,
    find_children,
)
from ansys.fluent.core.utils.fluent_version import FluentVersion
import ansys.units


class Setting:
    """Base class for setting objects."""

    def __init__(self, parent):
        self.parent = None if parent is None else weakref.proxy(parent)

    def get_attr(self, attr):
        attrs = self.get_attrs([attr])
        if attrs.get("active?"):
            return attrs[attr]
        else:
            raise RuntimeError("Object is not active")

    def get_attrs(self, attrs):
        active = self.attrs.get("active?", lambda self: True)(self)
        if active:
            return {attr: self.attrs[attr](self) for attr in attrs}
        else:
            return {"active?": False}

    attrs = {
        "active?": lambda self: True,
        "webui-release-active?": lambda self: True,
    }


class PrimitiveSetting(Setting):
    """Primitive setting objects."""

    value = None

    def get_state(self):
        return self.value

    def set_state(self, value):
        self.value = value

    @classmethod
    def get_static_info(cls):
        ret = {"type": cls.objtype}
        if cls.__doc__:
            ret["help"] = cls.__doc__
        return ret


class Bool(PrimitiveSetting):
    objtype = "boolean"


class Int(PrimitiveSetting):
    objtype = "integer"


class Real(PrimitiveSetting):
    objtype = "real"


class String(PrimitiveSetting):
    objtype = "string/symbol"


class BoolList(PrimitiveSetting):
    objtype = "boolean-list"


class IntList(PrimitiveSetting):
    objtype = "integer-list"


class RealList(PrimitiveSetting):
    objtype = "real-list"


class StringList(PrimitiveSetting):
    objtype = "string-list"


class Group(Setting):
    """Group objects."""

    objtype = "group"
    children = {}
    commands = {}

    def __init__(self, parent):
        super().__init__(parent)
        self.objs = {c: v(self) for c, v in self.children.items()}

    def get_state(self):
        ret = {}
        for c in self.children:
            cobj = self.objs[c]
            if cobj.get_attr("active?"):
                ret[c] = cobj.get_state()
        return ret

    def set_state(self, value):
        for c in self.children:
            v = value.get(c)
            if v is not None:
                self.objs[c].set_state(v)

    def get_child(self, c):
        return self.objs[c]

    def get_command(self, c):
        return self.commands[c](self)

    @classmethod
    def get_static_info(cls):
        ret = {"type": cls.objtype}
        if cls.__doc__:
            ret["help"] = cls.__doc__
        if cls.children:
            ret["children"] = {c: v.get_static_info() for c, v in cls.children.items()}
        if cls.commands:
            ret["commands"] = {c: v.get_static_info() for c, v in cls.commands.items()}
        return ret


class NamedObject(Setting, MutableMapping):
    """NamedObject class."""

    objtype = "named-object"
    commands = {}
    # To be overridden by child classes
    # child_object_type = None

    def __init__(self, parent):
        super().__init__(parent)
        self._objs = {}

    def __getitem__(self, name):
        return self._objs[name].get_state()

    def __setitem__(self, name, value):
        if name not in self._objs:
            self._objs[name] = self.child_object_type(self)
        return self._objs[name].set_state(value)

    def __delitem__(self, name):
        del self._objs[name]

    def __iter__(self):
        return iter(self._objs)

    def __len__(self):
        return len(self._objs)

    def get_child(self, c):
        return self._objs[c]

    def rename(self, new, old):
        self._objs = {(new if k == old else k): v for k, v in self._objs.items()}

    def get_object_names(self):
        return list(self._objs.keys())

    def get_command(self, c):
        return self.commands[c](self)

    def get_state(self):
        return {c: v.get_state() for c, v in self._objs.items()}

    def set_state(self, state):
        for k, v in state.items():
            self[k] = v

    @classmethod
    def get_static_info(cls):
        ret = {"type": cls.objtype}
        if cls.__doc__:
            ret["help"] = cls.__doc__
        ret["object-type"] = cls.child_object_type.get_static_info()
        if cls.commands:
            ret["commands"] = {c: v.get_static_info() for c, v in cls.commands.items()}
        try:
            if cls.user_creatable:
                ret["user_creatable"] = cls.user_creatable
        except AttributeError:
            ret["user_creatable"] = True
        return ret


class ListObject(Setting):
    """ListObject class."""

    objtype = "list-object"
    commands = {}
    # To be overridden by child classes
    # child_object_type = None

    def __init__(self, parent):
        super().__init__(parent)
        self._objs = []

    def __getitem__(self, index):
        return self._objs[index].get_state()

    def __setitem__(self, index, value):
        return self._objs[index].set_state(value)

    def __iter__(self):
        return iter(self._objs)

    def __len__(self):
        return len(self._objs)

    def size(self):
        return len(self._objs)

    def resize(self, new_size):
        if new_size > len(self._objs):
            for _ in range(len(self._objs), new_size):
                self._objs.append(self.child_object_type(self))
        elif new_size < len(self._objs):
            self._objs = self._objs[:new_size]

    def get_child(self, c):
        return self._objs[int(c)]

    def get_command(self, c):
        return self.commands[c](self)

    def get_state(self):
        return [x.get_state() for x in self._objs]

    def set_state(self, value):
        self.resize(len(value))
        for i, v in enumerate(value):
            self[i] = v

    @classmethod
    def get_static_info(cls):
        ret = {"type": cls.objtype}
        if cls.__doc__:
            ret["help"] = cls.__doc__
        ret["object-type"] = cls.child_object_type.get_static_info()
        if cls.commands:
            ret["commands"] = {c: v.get_static_info() for c, v in cls.commands.items()}
        return ret


class Command(Setting):
    """Command class."""

    objtype = "command"
    # To be overridden by child classes
    # arguments = None
    # cb = None

    def __init__(self, parent):
        self.attrs = super().attrs.copy()
        self.attrs["arguments-aliases"] = lambda self: {}
        super().__init__(parent)

    def __call__(self, **kwds):
        args = []
        for k, v in self.arguments.items():
            a = kwds.get(k, v(self).get_state())
            args.append(a)
        return self.cb(*args)

    @classmethod
    def get_static_info(cls):
        ret = {"type": cls.objtype}
        if cls.__doc__:
            ret["help"] = cls.__doc__
        if cls.arguments:
            ret["arguments"] = {
                c: v.get_static_info() for c, v in cls.arguments.items()
            }
        return ret


class Root(Group):
    """Root class."""

    class G1(Group):
        class S1(String):
            attrs = {
                "active?": lambda self: not self.parent.objs["b-3"].get_state(),
                "allowed-values": lambda self: ["foo", "bar"],
                "webui-release-active?": lambda self: True,
            }

        children = {
            "r-1": Real,
            "i-2": Int,
            "b-3": Bool,
            "s-4": S1,
        }

    class N1(NamedObject):
        class NC(Group):
            children = {
                "rl-1": RealList,
                "sl-1": StringList,
            }

        child_object_type = NC

    class L1(ListObject):
        class LC(Group):
            children = {
                "il-1": IntList,
                "bl-1": BoolList,
            }

        child_object_type = LC

    class Command1(Command):
        """Command1 class."""

        class A1(Real):
            value = 2.3

        class A2(Bool):
            value = True

        arguments = {
            "a-1": A1,
            "a-2": A2,
        }

        def cb(self, a1, a2):
            if a2 is True:
                self.parent.objs["g-1"].objs["r-1"].value += a1
            else:
                self.parent.objs["g-1"].objs["r-1"].value -= a1

    children = {
        "g-1": G1,
        "n-1": N1,
        "l-1": L1,
    }

    commands = {
        "c-1": Command1,
    }


class Proxy:
    """Proxy class."""

    root = Root

    def __init__(self):
        self.r = self.root(None)

    def get_obj(self, path):
        if not path:
            return self.r
        obj = self.r
        for c in path.split("/"):
            try:
                obj = obj.get_child(c)
            except KeyError:
                obj = obj.get_command(c)
        return obj

    def get_var(self, path):
        return self.get_obj(path).get_state()

    def set_var(self, path, value):
        return self.get_obj(path).set_state(value)

    def rename(self, path, new, old):
        return self.get_obj(path).rename(new, old)

    def create(self, path, name):
        self.get_obj(path)[name] = {}

    def delete(self, path, name):
        del self.get_obj(path)[name]

    def resize_list_object(self, path, size):
        return self.get_obj(path).resize(size)

    def get_list_size(self, path):
        return self.get_obj(path).size()

    def get_object_names(self, path):
        return self.get_obj(path).get_object_names()

    def execute_cmd(self, path, command, **kwds):
        return self.get_obj(path).get_command(command)(**kwds)

    def get_attrs(self, path, attrs, recursive=False):
        return self.get_obj(path).get_attrs(attrs)

    @classmethod
    def get_static_info(cls):
        return cls.root.get_static_info()

    def is_interactive_mode(self):
        return False

    def has_wildcard(self, name: str) -> bool:
        return False


def test_primitives():
    r = flobject.get_root(Proxy())
    r.g_1.r_1 = 3.2
    assert r.g_1.r_1() == 3.2
    r.g_1.i_2 = -3
    assert r.g_1.i_2() == -3
    r.g_1.b_3 = True
    assert r.g_1.b_3() is True
    r.g_1.b_3 = False
    assert r.g_1.b_3() is False
    r.g_1.s_4 = "foo"
    assert r.g_1.s_4() == "foo"


def test_group():
    r = flobject.get_root(Proxy())
    r.g_1 = {"r_1": 3.2, "i_2": -3, "b_3": False, "s_4": "foo"}
    assert r.g_1() == {"r_1": 3.2, "i_2": -3, "b_3": False, "s_4": "foo"}
    r.g_1 = {"s_4": "bar"}
    assert r.g_1() == {"r_1": 3.2, "i_2": -3, "b_3": False, "s_4": "bar"}
    r.g_1.i_2 = 4
    assert r.g_1() == {"r_1": 3.2, "i_2": 4, "b_3": False, "s_4": "bar"}


def test_settings_input_set_state():
    r = flobject.get_root(Proxy())
    r.g_1 = {"r_1": 3.2, "i_2": -3, "b_3": False, "s_4": "foo"}
    r.g_1.set_state(r_1=3.2, i_2=-3, b_3=False, s_4="foo")
    assert r.g_1() == {"r_1": 3.2, "i_2": -3, "b_3": False, "s_4": "foo"}
    r.g_1.set_state(s_4="bar")
    assert r.g_1() == {"r_1": 3.2, "i_2": -3, "b_3": False, "s_4": "bar"}
    r.g_1.set_state(i_2=4)
    assert r.g_1() == {"r_1": 3.2, "i_2": 4, "b_3": False, "s_4": "bar"}


def test_settings_input():
    r = flobject.get_root(Proxy())
    r.g_1 = {"r_1": 3.2, "i_2": -3, "b_3": False, "s_4": "foo"}
    r.g_1(r_1=3.2, i_2=-3, b_3=False, s_4="foo")
    assert r.g_1() == {"r_1": 3.2, "i_2": -3, "b_3": False, "s_4": "foo"}
    r.g_1(s_4="bar")
    assert r.g_1() == {"r_1": 3.2, "i_2": -3, "b_3": False, "s_4": "bar"}
    r.g_1(i_2=4)
    assert r.g_1() == {"r_1": 3.2, "i_2": 4, "b_3": False, "s_4": "bar"}


def test_named_object():
    r = flobject.get_root(Proxy())
    assert r.n_1.get_object_names() == []
    r.n_1["n1"] = {}
    r.n_1["n2"] = {}
    assert r.n_1.get_object_names() == ["n1", "n2"]
    r.n_1.create("n4")
    assert r.n_1.get_object_names() == ["n1", "n2", "n4"]
    del r.n_1["n1"]
    assert r.n_1.get_object_names() == ["n2", "n4"]
    r.n_1["n1"] = {"rl_1": [1.2, 3.4], "sl_1": ["foo", "bar"]}
    assert r.n_1["n1"]() == {"rl_1": [1.2, 3.4], "sl_1": ["foo", "bar"]}
    r.n_1 = {"n5": {"rl_1": [4.3, 2.1], "sl_1": ["oof", "rab"]}}
    assert r.n_1.get_object_names() == ["n2", "n4", "n1", "n5"]
    assert r.n_1["n5"]() == {"rl_1": [4.3, 2.1], "sl_1": ["oof", "rab"]}


def test_list_object():
    r = flobject.get_root(Proxy())
    assert r.l_1.get_size() == 0
    r.l_1 = [
        {"il_1": None, "bl_1": None},
        {"il_1": None, "bl_1": None},
    ]
    r.l_1[1].il_1 = [1, 2]
    assert r.l_1() == [
        {"il_1": None, "bl_1": None},
        {"il_1": [1, 2], "bl_1": None},
    ]
    r.l_1 = [{"il_1": [3], "bl_1": [True, False]}]
    assert r.l_1() == [{"il_1": [3], "bl_1": [True, False]}]


def test_command():
    r = flobject.get_root(Proxy())
    r.g_1.r_1 = 2.4
    r.c_1()
    assert r.g_1.r_1() == 2.4 + 2.3
    r.c_1(a_2=False)
    assert r.g_1.r_1() == 2.4 + 2.3 - 2.3
    r.c_1(a_1=3.2, a_2=True)
    assert r.g_1.r_1() == 2.4 + 2.3 - 2.3 + 3.2
    r.c_1(a_1=4.5, a_2=False)
    assert r.g_1.r_1() == 2.4 + 2.3 - 2.3 + 3.2 - 4.5


def test_attrs():
    r = flobject.get_root(Proxy())
    r._setattr("version", "251")
    assert r.g_1.s_4.get_attr("active?")
    assert r.g_1.s_4.get_attr("allowed-values") == ["foo", "bar"]
    r.g_1.b_3 = True
    assert not r.g_1.s_4.get_attr("active?")
    with pytest.raises(InactiveObjectError):
        r.g_1.s_4.get_attr("allowed-values")


# The following test is commented out as codegen module is not packaged in the
# install
def _disabled_test_settings_gen():
    info = Proxy().get_static_info()
    cls, _ = flobject.get_cls("", info)
    f = io.StringIO()
    ansys.fluent.core.codegen.settingsgen.write_settings_classes(f, cls, info)
    assert (
        f.getvalue()
        == '''###
### THIS FILE IS AUTOGENERATED! DO NOT MODIFY!

###
from ansys.fluent.solver.flobject import *

SHASH = "0392eb93ff1d5f9dd50ef9fddc74581ad3e8f74c34c569b6a1a6f1b57753d5ad"

class root(Group):
    """
    Root class
    """
    fluent_name = ""
    child_names = \\
        ['g_1', 'n_1', 'l_1']

    class g_1(Group):
        """
        'g_1' child of 'root' object
        """
        fluent_name = "g-1"
        child_names = \\
            ['r_1', 'i_2', 'b_3', 's_4']

        class r_1(Real):
            """
            'r_1' child of 'g_1' object
            """
            fluent_name = "r-1"

        class i_2(Integer):
            """
            'i_2' child of 'g_1' object
            """
            fluent_name = "i-2"

        class b_3(Boolean):
            """
            'b_3' child of 'g_1' object
            """
            fluent_name = "b-3"

        class s_4(String):
            """
            's_4' child of 'g_1' object
            """
            fluent_name = "s-4"

    class n_1(NamedObject):
        """
        'n_1' child of 'root' object
        """
        fluent_name = "n-1"

        class child_object_type(Group):
            """
            'child_object_type' child of 'n_1' object
            """
            fluent_name = "child-object-type"
            child_names = \\
                ['rl_1', 'sl_1']

            class rl_1(RealList):
                """
                'rl_1' child of 'child_object_type' object
                """
                fluent_name = "rl-1"

            class sl_1(StringList):
                """
                'sl_1' child of 'child_object_type' object
                """
                fluent_name = "sl-1"

    class l_1(ListObject):
        """
        'l_1' child of 'root' object
        """
        fluent_name = "l-1"

        class child_object_type(Group):
            """
            'child_object_type' child of 'l_1' object
            """
            fluent_name = "child-object-type"
            child_names = \\
                ['il_1', 'bl_1']

            class il_1(IntegerList):
                """
                'il_1' child of 'child_object_type' object
                """
                fluent_name = "il-1"

            class bl_1(BooleanList):
                """
                'bl_1' child of 'child_object_type' object
                """
                fluent_name = "bl-1"
    command_names = \\
        ['c_1']

    class c_1(Command):
        """
        Command1 class

        Parameters
        ----------
            a_1 : real
                'a_1' child of 'c_1' object
            a_2 : bool
                'a_2' child of 'c_1' object

        """
        fluent_name = "c-1"
        argument_names = \\
            ['a_1', 'a_2']

        class a_1(Real):
            """
            'a_1' child of 'c_1' object
            """
            fluent_name = "a-1"

        class a_2(Boolean):
            """
            'a_2' child of 'c_1' object
            """
            fluent_name = "a-2"
'''
    )  # noqa: W293


@pytest.mark.fluent_version("latest")
def test_accessor_methods_on_settings_object(static_mixer_settings_session):
    solver = static_mixer_settings_session

    existing = solver.file.read.file_type.get_attr("allowed-values")
    modified = solver.file.read.file_type.allowed_values()
    assert existing == modified

    existing = solver.file.read.file_type.get_attr("read-only?", bool)
    modified = solver.file.read.file_type.is_read_only()

    assert existing == modified

    velocity_inlet = solver.setup.boundary_conditions.velocity_inlet
    existing = velocity_inlet.get_attr("user-creatable?", bool)
    modified = velocity_inlet.user_creatable()
    assert existing == modified

    if solver.get_fluent_version() < FluentVersion.v242:
        turbulent_viscosity_ratio = velocity_inlet[
            "inlet1"
        ].turbulence.turbulent_viscosity_ratio_real

        path = '<session>.setup.boundary_conditions.velocity_inlet["inlet1"].turbulence.turbulent_viscosity_ratio_real'
        name = "turbulent_viscosity_ratio_real"

    else:
        turbulent_viscosity_ratio = velocity_inlet[
            "inlet1"
        ].turbulence.turbulent_viscosity_ratio

        if solver.get_fluent_version() >= FluentVersion.v251:
            path = '<session>.settings.setup.boundary_conditions.velocity_inlet["inlet1"].turbulence.turbulent_viscosity_ratio'
        else:
            path = '<session>.setup.boundary_conditions.velocity_inlet["inlet1"].turbulence.turbulent_viscosity_ratio'
        name = "turbulent_viscosity_ratio"

    assert turbulent_viscosity_ratio.python_path == path
    assert turbulent_viscosity_ratio.python_name == name

    assert turbulent_viscosity_ratio.default_value() == 10
    assert turbulent_viscosity_ratio.get_attr("min") == 0

    assert turbulent_viscosity_ratio.get_attr("max") is False
    assert turbulent_viscosity_ratio.max() is None

    default_attrs = solver.setup.boundary_conditions.velocity_inlet["inlet1"].get_attrs(
        ["default"], recursive=True
    )
    assert count_key_recursive(default_attrs, "default") > 5

    mesh = solver.results.graphics.mesh.create("mesh-1")
    if solver.get_fluent_version() < FluentVersion.v242:
        assert mesh.name.is_read_only()
    else:
        assert not mesh.name.is_read_only()

    assert solver.results.graphics.mesh.get_object_names() == ["mesh-1"]

    solver.results.graphics.mesh["mesh-1"].rename("mesh_new")
    assert solver.results.graphics.mesh.get_object_names() == ["mesh_new"]

    solver.results.graphics.mesh.rename(new="mesh_242", old="mesh_new")
    assert solver.results.graphics.mesh.get_object_names() == ["mesh_242"]


@pytest.mark.fluent_version("latest")
def test_accessor_methods_on_settings_object_types(static_mixer_settings_session):
    solver = static_mixer_settings_session

    assert solver.setup.general.solver.type.allowed_values() == [
        "pressure-based",
        "density-based-implicit",
        "density-based-explicit",
    ]
    accuracy_control = (
        solver.setup.models.discrete_phase.numerics.tracking.accuracy_control
    )
    if solver.get_fluent_version() < FluentVersion.v241:
        max_refinements = accuracy_control.max_number_of_refinements
    else:
        max_refinements = accuracy_control.max_num_refinements

    assert max_refinements.min() == 0
    assert max_refinements.max() == 1000000
    assert max_refinements.get_attr("max") == 1000000


@pytest.mark.fluent_version("==24.1")
@pytest.mark.codegen_required
def test_find_children_from_settings_root(static_mixer_settings_session):
    setup_cls = static_mixer_settings_session.setup.__class__
    assert len(find_children(setup_cls())) >= 10000
    assert len(find_children(setup_cls(), "gen*")) >= 9
    assert set(find_children(setup_cls(), "general*")) >= {
        "general",
        "models/discrete_phase/general_settings",
        "models/virtual_blade_model/rotor/general",
    }
    assert set(find_children(setup_cls(), "general")) >= {
        "general",
        "models/virtual_blade_model/rotor/general",
    }
    assert any(
        path
        for path in find_children(setup_cls(), "*gen")
        if path.endswith("p_backflow_spec_gen")
    )


@pytest.mark.fluent_version("latest")
def test_find_children_from_fluent_solver_session(static_mixer_settings_session):
    setup_children = find_children(static_mixer_settings_session.setup)
    load_mixer = static_mixer_settings_session.setup
    assert len(setup_children) >= 18514

    viscous = load_mixer.models.viscous
    assert len(find_children(viscous, "prod*")) > 0

    assert any(
        path
        for path in find_children(
            load_mixer.boundary_conditions.pressure_outlet, "*_dir_*"
        )
        if path.endswith("geom_dir_spec")
    )

    if static_mixer_settings_session.get_fluent_version() < FluentVersion.v242:
        assert set(
            find_children(
                load_mixer.materials.fluid["air"].density.piecewise_polynomial
            )
        ) >= {
            "minimum",
            "maximum",
            "coefficients",
        }
    else:
        assert set(
            find_children(
                load_mixer.materials.fluid["air"].density.piecewise_polynomial
            )
        ) >= {
            "range/minimum",
            "range/maximum",
            "range/coefficients",
        }


@pytest.mark.fluent_version(">=24.1")
def test_settings_wild_card_access(new_solver_session) -> None:
    solver = new_solver_session

    case_path = download_file("elbow_source_terms.cas.h5", "pyfluent/mixing_elbow")
    solver.file.read_case(file_name=case_path)

    solver.solution.initialization.hybrid_initialize()

    if solver.get_fluent_version() >= FluentVersion.v251:
        assert (
            solver.setup.boundary_conditions.velocity_inlet[
                "*1"
            ].momentum.velocity_magnitude.value()["inlet1"]["momentum"][
                "velocity_magnitude"
            ][
                "value"
            ]
            == solver.setup.boundary_conditions.velocity_inlet[
                "inlet1"
            ].momentum.velocity.value()
        )
    else:
        assert (
            solver.setup.boundary_conditions.velocity_inlet[
                "*1"
            ].momentum.velocity.value()["inlet1"]["momentum"]["velocity"]["value"]
            == solver.setup.boundary_conditions.velocity_inlet[
                "inlet1"
            ].momentum.velocity.value()
        )

    assert solver.setup.boundary_conditions.wall["*"]()

    with pytest.raises(AttributeError) as msg:
        solver.setup.boundary_conditions.velocity_inlet["*1"].inlet1()
    assert msg.value.args[0] == "'velocity_inlet' has no attribute 'inlet1'.\n"

    with pytest.raises(KeyError) as msg:
        solver.setup.boundary_conditions.velocity_inlet["inlet-1"]
    assert (
        msg.value.args[0] == "'velocity_inlet' has no attribute 'inlet-1'.\n"
        "The most similar names are: inlet1, inlet2."
    )


@pytest.mark.fluent_version(">=25.1")
def test_settings_matching_names(new_solver_session) -> None:
    solver = new_solver_session

    case_path = download_file("elbow_source_terms.cas.h5", "pyfluent/mixing_elbow")
    solver.file.read_case(file_name=case_path)

    solver.solution.initialization.hybrid_initialize()

    with pytest.raises(AttributeError) as msg:
        solver.setup.mod

    assert msg.value.args[0].startswith(
        "'setup' object has no attribute 'mod'.\n\n" "The most similar API names are:\n"
    )

    assert len(msg.value.args[0].split("\n")) > 5

    with pytest.raises(ValueError) as msg:
        solver.setup.models.viscous.model = "k_epsilon"

    assert (
        msg.value.args[0] == "'model' has no attribute 'k_epsilon'.\n"
        "The most similar names are: k-epsilon."
    )


@pytest.mark.codegen_required
@pytest.mark.fluent_version(">=23.2")
def test_settings_api_names_exception(new_solver_session):
    solver = new_solver_session

    case_path = download_file("mixing_elbow.msh.h5", "pyfluent/mixing_elbow")
    solver.file.read_case(file_name=case_path)

    with pytest.raises(RuntimeError):
        solver.setup.boundary_conditions["cold-inlet"].name = "hot-inlet"


@pytest.mark.fluent_version(">=24.2")
def test_accessor_methods_on_settings_objects(new_solver_session):
    solver = new_solver_session
    root = solver.settings

    nodes = {}
    expected_type_list = [
        "Boolean",
        "String",
        "Real",
        "Integer",
        "RealList",
        "ListObject",
    ]
    type_list = expected_type_list.copy()

    get_child_nodes(root, nodes, type_list)

    for type_data in expected_type_list:
        if type_data == "Boolean":
            assert {
                "is_active",
                "is_read_only",
                "default_value",
                "get_state",
                "set_state",
            }.issubset(set(dir(nodes[type_data])))
            assert nodes[type_data].is_read_only() in [True, False]
            assert nodes[type_data].is_active() in [True, False]

        elif type_data in ["Integer", "Real", "IntegerList", "RealList"]:
            assert {
                "is_active",
                "is_read_only",
                "default_value",
                "get_state",
                "set_state",
                "min",
                "max",
            }.issubset(set(dir(nodes[type_data])))
            assert not {"allowed_values"}.issubset(set(dir(nodes[type_data])))
            assert nodes[type_data].is_read_only() in [True, False]
            assert nodes[type_data].is_active() in [True, False]

        elif type_data in ["String", "StringList", "Filename"]:
            assert {
                "is_active",
                "is_read_only",
                "default_value",
                "get_state",
                "set_state",
                "allowed_values",
            }.issubset(set(dir(nodes[type_data])))
            assert not {"min", "max"}.issubset(set(dir(nodes[type_data])))
            assert nodes[type_data].is_read_only() in [True, False]
            assert nodes[type_data].is_active() in [True, False]

        elif type_data == "ListObject":
            assert {"is_active", "is_read_only", "get_state", "set_state"}.issubset(
                set(dir(nodes[type_data]))
            )
            assert nodes[type_data].is_read_only() in [True, False]
            assert nodes[type_data].is_active() in [True, False]


def get_child_nodes(node, nodes, type_list):
    if node.is_active():
        if isinstance(node, flobject.Group):
            for item in node.child_names:
                get_child_nodes(getattr(node, item), nodes, type_list)
        else:
            node_type = node.__class__.__bases__[0].__name__
            if node_type in type_list:
                type_list.remove(node_type)
                nodes[node_type] = node
                if not type_list:
                    return


@pytest.mark.fluent_version("latest")
def test_strings_with_allowed_values(static_mixer_settings_session):
    solver = static_mixer_settings_session

    with pytest.raises(AttributeError) as e:
        solver.file.auto_save.root_name.allowed_values()
    assert e.value.args[0] == "'root_name' object has no attribute 'allowed_values'"

    string_with_allowed_values = solver.setup.general.solver.type.allowed_values()
    assert string_with_allowed_values == [
        "pressure-based",
        "density-based-implicit",
        "density-based-explicit",
    ]


@pytest.mark.fluent_version(">=24.2")
def test_parent_class_attributes(static_mixer_settings_session):
    solver = static_mixer_settings_session
    assert solver.setup.models.energy.enabled
    with pytest.raises(AttributeError):
        solver.setup.models.energy.__class__.enabled


def _check_vector_units(obj, units):
    assert obj.units() == units
    state_with_units = obj.state_with_units()
    state = obj.get_state()
    assert len(state_with_units) == 2
    assert len(state) == len(state_with_units[0])
    assert all(x == y for x, y in zip(state, state_with_units[0]))
    assert units == state_with_units[1]
    assert obj.as_quantity() == ansys.units.Quantity(obj.get_state(), units)


@pytest.mark.fluent_version(">=24.1")
def test_ansys_units_integration(mixing_elbow_settings_session):
    solver = mixing_elbow_settings_session
    assert isinstance(solver.settings.state_with_units(), dict)
    hot_inlet = solver.setup.boundary_conditions.velocity_inlet["hot-inlet"]
    turbulence = hot_inlet.turbulence
    turbulence.turbulent_specification = "Intensity and Hydraulic Diameter"
    hydraulic_diameter = turbulence.hydraulic_diameter
    hydraulic_diameter.set_state("1 [in]")
    assert hydraulic_diameter() == "1 [in]"
    assert hydraulic_diameter.as_quantity() is None
    assert hydraulic_diameter.state_with_units() == ("1 [in]", "m")
    assert hydraulic_diameter.units() == "m"
    turbulent_intensity = turbulence.turbulent_intensity
    turbulent_intensity.set_state(0.2)
    assert turbulent_intensity() == 0.2
    assert turbulent_intensity.as_quantity() == ansys.units.Quantity(0.2, "")
    turbulent_intensity.set_state(ansys.units.Quantity(0.1, ""))
    assert turbulent_intensity.state_with_units() == (0.1, "")
    hydraulic_diameter.set_state(1)
    assert hydraulic_diameter.as_quantity() == ansys.units.Quantity(1, "m")
    assert hydraulic_diameter.state_with_units() == (1.0, "m")
    assert hydraulic_diameter.units() == "m"
    hydraulic_diameter.set_state(ansys.units.Quantity(1, "in"))
    assert hydraulic_diameter.as_quantity() == ansys.units.Quantity(0.0254, "m")
    assert hydraulic_diameter.state_with_units() == (0.0254, "m")
    assert hydraulic_diameter.units() == "m"
    assert hydraulic_diameter() == 0.0254
    velocity = ansys.units.Quantity(
        12.0, ansys.units.UnitRegistry().ft
    ) / ansys.units.Quantity(3.0, ansys.units.UnitRegistry().s)
    hot_inlet.momentum.velocity.value = velocity
    assert hot_inlet.momentum.velocity.value.as_quantity() == velocity
    velocity = (1.0, "m s^-1")
    hot_inlet.momentum.velocity = velocity
    assert hot_inlet.momentum.velocity.value.state_with_units() == velocity
    velocity = ansys.units.Quantity(12.0, "m s^-1")
    hot_inlet.momentum.velocity = velocity
    assert hot_inlet.momentum.velocity.value() == velocity.value
    assert hot_inlet.momentum.velocity.value.as_quantity() == velocity
    assert hot_inlet.momentum.velocity.state_with_units() == {
        "option": "value",
        "value": (12.0, "m s^-1"),
    }
    clip_factor = solver.setup.models.viscous.options.production_limiter.clip_factor
    clip_factor.set_state(1.2)
    assert clip_factor() == 1.2
    assert clip_factor.as_quantity() == ansys.units.Quantity(1.2, "")
    assert clip_factor.state_with_units() == (1.2, "")
    assert clip_factor.units() == ""
    clip_factor.set_state(ansys.units.Quantity(1.8, ""))
    assert clip_factor.as_quantity() == ansys.units.Quantity(1.8, "")
    assert clip_factor.state_with_units() == (1.8, "")
    assert clip_factor.units() == ""

    _check_vector_units(
        solver.setup.general.operating_conditions.reference_pressure_location, "m"
    )
    _check_vector_units(
        solver.setup.reference_frames[
            "global"
        ].initial_state.orientation.first_axis.axis_to.vector,
        "",
    )


@pytest.mark.fluent_version(">=24.2")
def test_ansys_units_integration_nested_state(mixing_elbow_settings_session):
    solver = mixing_elbow_settings_session

    hot_inlet = solver.setup.boundary_conditions.velocity_inlet["hot-inlet"]

    assert hot_inlet.state_with_units() == {
        "momentum": {
            "initial_gauge_pressure": {"option": "value", "value": (0, "Pa")},
            "reference_frame": "Absolute",
            "velocity": {"option": "value", "value": (0, "m s^-1")},
            "velocity_specification_method": "Magnitude, Normal to Boundary",
        },
        "name": "hot-inlet",
        "turbulence": {
            "turbulent_intensity": (0.05, ""),
            "turbulent_specification": "Intensity and Viscosity Ratio",
            "turbulent_viscosity_ratio": (10, None),
        },
    } or {
        "momentum": {
            "initial_gauge_pressure": {"option": "value", "value": (0, "Pa")},
            "reference_frame": "Absolute",
            "velocity": {"option": "value", "value": (0, "m s^-1")},
            "velocity_specification_method": "Magnitude, Normal to Boundary",
        },
        "name": "hot-inlet",
        "turbulence": {
            "turbulent_specification": "Intensity and Viscosity Ratio",
            "turbulent_intensity": (0.05, ""),
            "turbulent_viscosity_ratio": (10, None),
        },
    }


@pytest.mark.fluent_version(">=24.2")
def test_bug_1001124_quantity_assignment(mixing_elbow_settings_session):
    speed = ansys.units.Quantity(100, "m s^-1")
    solver = mixing_elbow_settings_session
    solver.setup.boundary_conditions.velocity_inlet[
        "hot-inlet"
    ].momentum.velocity.value = speed.value
    assert (
        solver.setup.boundary_conditions.velocity_inlet[
            "hot-inlet"
        ].momentum.velocity.value()
        == speed.value
    )
    solver.setup.boundary_conditions.velocity_inlet["hot-inlet"].momentum.velocity = (
        speed
    )
    assert (
        solver.setup.boundary_conditions.velocity_inlet[
            "hot-inlet"
        ].momentum.velocity.value()
        == speed.value
    )


def test_assert_type():
    types = [
        bool,
        int,
        flobject.RealType,
        str,
        flobject.BoolListType,
        flobject.IntListType,
        flobject.RealListType,
        flobject.StringListType,
        flobject.RealVectorType,
        flobject.DictStateType,
    ]
    vals = [
        False,
        1,
        1.0,
        "a",
        [False, True],
        [1, 2],
        [1.0, 2.0],
        ["a", "b"],
        (1.0, 2.0, 3.0),
        {"a": 1},
    ]
    subtypes = {
        bool: (int,),
        str: (flobject.RealType,),
        flobject.BoolListType: (flobject.IntListType,),
        flobject.StringListType: (flobject.RealListType,),
    }
    for i_t, tp in enumerate(types):
        for i_v, val in enumerate(vals):
            if i_t == i_v:
                flobject.assert_type(val, tp)
            else:
                subtype = subtypes.get(types[i_v])
                if subtype and types[i_t] in subtype:
                    flobject.assert_type(val, tp)
                else:
                    with pytest.raises(TypeError):
                        flobject.assert_type(val, tp)


def test_static_info_hash_identity(new_solver_session):
    solver = new_solver_session
    hash1 = _gethash(solver._settings_service.get_static_info())
    hash2 = _gethash(solver._settings_service.get_static_info())
    assert hash1 == hash2


@pytest.mark.codegen_required
def test_no_hash_mismatch(new_solver_session, caplog):
    caplog.clear()
    new_solver_session.setup
    assert all(["Mismatch" not in record.message for record in caplog.records])


@pytest.mark.fluent_version(">=24.2")
def test_default_argument_names_for_commands(static_mixer_settings_session):
    solver = static_mixer_settings_session

    if solver.get_fluent_version() >= FluentVersion.v251:
        assert set(solver.results.graphics.contour.command_names) == {
            "create",
            "delete",
            "rename",
            "list",
            "list_properties",
            "make_a_copy",
            "display",
            "add_to_graphics",
            "clear_history",
        }
    else:
        assert set(solver.results.graphics.contour.command_names) == {
            "delete",
            "rename",
            "list",
            "list_properties",
            "make_a_copy",
            "display",
            "copy",
            "add_to_graphics",
            "clear_history",
        }

    assert solver.results.graphics.contour.rename.argument_names == ["new", "old"]
    assert solver.results.graphics.contour.delete.argument_names == ["name_list"]
    # The following is the default behavior when no arguments are associated with the command.
    assert solver.results.graphics.contour.list.argument_names == []
