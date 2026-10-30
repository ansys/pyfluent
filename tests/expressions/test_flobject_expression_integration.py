# Copyright (C) 2021 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT

"""Tests for the generic settings-expression protocol in ``flobject``.

These tests verify -- without a live Fluent session -- that the settings layer
accepts "expression objects" through a domain-neutral protocol
(``__settings_str__`` / ``__settings_kind__`` / ``__settings_dimensions__``)
rather than any Fluent-specific hook or hard-coded path. Specifically:

* A :class:`Textual` leaf (``String`` / ``Filename``) accepts an expression
  object *anywhere* and stores its rendered string.
* A :class:`RealNumerical` leaf (``Real`` / ``RealList``) accepts an expression
  object wherever expression strings are permitted.
* Quantity-type validation (structural kind and physical dimension) runs
  *before* the expression is rendered to a string.
* Plain strings and ``VariableDescriptor`` values keep working as before.
"""

import pytest

from ansys.fluent.core.offline.expressions import ExpressionBuilder
from ansys.fluent.core.offline.expressions._ast import Quantity
from ansys.fluent.core.solver.flobject import (
    Filename,
    FilenameList,
    Group,
    Numerical,
    Real,
    RealList,
    RealNumerical,
    SettingsBase,
    String,
    StringList,
    Textual,
    _is_settings_expression,
    _normalize_dimensions,
    _render_settings_expression,
    _render_settings_expression_list,
    _settings_expression_to_scheme,
    _textual_list_set_state,
)
from ansys.units import VariableCatalog as V

# --------------------------------------------------------------------------- #
# Test doubles                                                                #
# --------------------------------------------------------------------------- #


class _FakeTextualLeaf:
    """Minimal stand-in for a ``String``/``Filename`` settings leaf.

    Captures whatever ``base_set_state`` receives so tests can assert on the
    value the settings layer would have stored.
    """

    _has_migration_adapter = False
    _expression_kinds = Textual._expression_kinds
    python_path = "setup.named_expressions['x'].definition"

    def __init__(self):
        self.captured = None

    def base_set_state(self, state=None, **kwargs):
        self.captured = state
        return state

    def set_state_via(self, state):
        """Route through the real ``Textual.set_state`` for this fake leaf."""
        return Textual.set_state(self, state)


class _FakeRealLeaf:
    """Minimal stand-in for a ``Real`` settings leaf with a fixed unit.

    ``units()`` mirrors :meth:`RealNumerical.units`, enabling the dimensional
    check. ``_expression_kinds`` is inherited from :class:`RealNumerical`.
    """

    _expression_kinds = RealNumerical._expression_kinds
    python_path = "setup.boundary_conditions['inlet'].pressure"

    def __init__(self, units="Pa"):
        self._units = units
        self.captured = None
        self.units_calls = 0

    def units(self):
        # Count lookups: on a real leaf this is an uncached RPC, so a bulk
        # assignment must resolve it once, not once per element.
        self.units_calls += 1
        return self._units

    def base_set_state(self, state=None, **kwargs):
        self.captured = state
        return state

    def set_state_via(self, state):
        """Route through the real ``RealNumerical.set_state`` for this fake leaf."""
        return RealNumerical.set_state(self, state)


class _FakeRealListLeaf(_FakeRealLeaf):
    """Minimal stand-in for a ``RealList`` leaf (a container of reals).

    Mirrors :class:`RealList`, which widens the accepted kinds to also allow a
    single vector-valued expression for the whole-list assignment while sharing
    :meth:`RealNumerical.set_state`.
    """

    _expression_kinds = ("scalar", "vector", "quantity")
    _element_expression_kinds = ("scalar", "quantity")
    python_path = "setup.boundary_conditions['inlet'].flow_direction"


@pytest.fixture
def builder():
    return ExpressionBuilder()  # settings=None -- offline construction


@pytest.fixture
def pressure_expr(builder):
    """A scalar, pressure-dimensioned reduction expression."""
    return builder.reductions.area_ave(
        expression=V.ABSOLUTE_PRESSURE, locations=["inlet1"]
    )


# --------------------------------------------------------------------------- #
# Protocol detection / helpers                                                #
# --------------------------------------------------------------------------- #


def test_expr_implements_settings_protocol(pressure_expr):
    assert _is_settings_expression(pressure_expr) is True
    assert pressure_expr.__settings_str__() == "AreaAve(AbsolutePressure,['inlet1'])"
    assert pressure_expr.__settings_kind__() == "scalar"


def test_plain_values_are_not_settings_expressions():
    assert _is_settings_expression("AbsolutePressure") is False
    assert _is_settings_expression(3.14) is False
    assert _is_settings_expression(V.ABSOLUTE_PRESSURE) is False


def test_normalize_dimensions_accepts_name_and_enum_keys():
    import ansys.units

    from_quantity = _normalize_dimensions(ansys.units.Quantity(1, "Pa").dimensions)
    from_names = _normalize_dimensions({"MASS": 1.0, "LENGTH": -1.0, "TIME": -2.0})
    assert from_quantity == from_names
    # Zero exponents are dropped.
    assert _normalize_dimensions({"MASS": 0.0, "LENGTH": 1.0}) == {"LENGTH": 1.0}


# --------------------------------------------------------------------------- #
# Textual leaves accept expression objects anywhere                           #
# --------------------------------------------------------------------------- #


def test_textual_leaf_accepts_expression_object(pressure_expr):
    leaf = _FakeTextualLeaf()
    Textual.set_state(leaf, pressure_expr)
    assert leaf.captured == "AreaAve(AbsolutePressure,['inlet1'])"


def test_textual_leaf_still_accepts_string():
    leaf = _FakeTextualLeaf()
    Textual.set_state(leaf, "AreaAve(AbsolutePressure, ['inlet1'])")
    assert leaf.captured == "AreaAve(AbsolutePressure, ['inlet1'])"


def test_textual_leaf_still_accepts_variable_descriptor():
    leaf = _FakeTextualLeaf()
    # A VariableDescriptor does not implement the expression protocol, so it is
    # handled by Textual's own field-name strategy: only that a string was
    # captured matters here, not its exact spelling.
    Textual.set_state(leaf, V.ABSOLUTE_PRESSURE)
    assert isinstance(leaf.captured, str) and leaf.captured


def test_textual_leaf_rejects_location_list_expression(builder):
    leaf = _FakeTextualLeaf()
    location_list = builder.locations(["inlet1", "inlet2"])
    with pytest.raises(TypeError, match="kind 'location_list'"):
        Textual.set_state(leaf, location_list)


# --------------------------------------------------------------------------- #
# Filename leaves route through the protocol before their inherited setter     #
# --------------------------------------------------------------------------- #


def test_filename_leaf_renders_expression_object(pressure_expr, monkeypatch):
    # ``Filename`` resolves ``set_state`` via ``SettingsBase`` in the MRO, so it
    # must explicitly route protocol objects through the expression helper
    # instead of serializing them with ``str()``.
    captured = {}
    monkeypatch.setattr(
        Filename,
        "base_set_state",
        lambda self, state=None, **kwargs: captured.__setitem__("state", state),
    )
    leaf = Filename(name="x")
    leaf.set_state(pressure_expr)
    assert captured["state"] == "AreaAve(AbsolutePressure,['inlet1'])"


def test_filename_leaf_still_accepts_plain_string(monkeypatch):
    captured = {}
    monkeypatch.setattr(
        Filename,
        "base_set_state",
        lambda self, state=None, **kwargs: captured.__setitem__("state", state),
    )
    leaf = Filename(name="x")
    leaf.set_state("input.cas.h5")
    assert captured["state"] == "input.cas.h5"


def test_filename_leaf_rejects_location_list_expression(builder, monkeypatch):
    captured = {}
    monkeypatch.setattr(
        Filename,
        "base_set_state",
        lambda self, state=None, **kwargs: captured.__setitem__("state", state),
    )
    leaf = Filename(name="x")
    location_list = builder.locations(["inlet1", "inlet2"])
    with pytest.raises(TypeError, match="kind 'location_list'"):
        leaf.set_state(location_list)
    assert captured == {}  # never rendered / stored


# --------------------------------------------------------------------------- #
# Textual list leaves render each expression element via the protocol          #
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize("list_cls", [StringList, FilenameList])
def test_textual_list_renders_expression_elements(list_cls, pressure_expr, monkeypatch):
    # ``StringList`` / ``FilenameList`` resolve ``set_state`` via ``SettingsBase``
    # in the MRO, so (like ``Filename``) they must route each expression element
    # through the protocol instead of serializing it with ``str()``.
    captured = {}
    monkeypatch.setattr(
        list_cls,
        "base_set_state",
        lambda self, state=None, **kwargs: captured.__setitem__("state", state),
    )
    leaf = list_cls(name="x")
    leaf.set_state(["a.txt", pressure_expr, "b.txt"])
    assert captured["state"] == [
        "a.txt",
        "AreaAve(AbsolutePressure,['inlet1'])",
        "b.txt",
    ]


@pytest.mark.parametrize("list_cls", [StringList, FilenameList])
def test_textual_list_still_accepts_plain_list(list_cls, monkeypatch):
    captured = {}
    monkeypatch.setattr(
        list_cls,
        "base_set_state",
        lambda self, state=None, **kwargs: captured.__setitem__("state", state),
    )
    leaf = list_cls(name="x")
    leaf.set_state(["a.txt", "b.txt"])
    assert captured["state"] == ["a.txt", "b.txt"]


@pytest.mark.parametrize("list_cls", [StringList, FilenameList])
def test_textual_list_rejects_location_list_element(list_cls, builder, monkeypatch):
    captured = {}
    monkeypatch.setattr(
        list_cls,
        "base_set_state",
        lambda self, state=None, **kwargs: captured.__setitem__("state", state),
    )
    leaf = list_cls(name="x")
    location_list = builder.locations(["inlet1", "inlet2"])
    with pytest.raises(TypeError, match="kind 'location_list'"):
        leaf.set_state([location_list])
    assert captured == {}  # never rendered / stored


# --------------------------------------------------------------------------- #
# Real leaves accept expression objects (the new capability)                  #
# --------------------------------------------------------------------------- #


def test_real_leaf_accepts_expression_object(pressure_expr):
    leaf = _FakeRealLeaf(units="Pa")
    RealNumerical.set_state(leaf, pressure_expr)
    assert leaf.captured == "AreaAve(AbsolutePressure,['inlet1'])"


def test_real_leaf_still_accepts_plain_float():
    leaf = _FakeRealLeaf(units="Pa")
    RealNumerical.set_state(leaf, 101325.0)
    assert leaf.captured == 101325.0


# --------------------------------------------------------------------------- #
# Quantity-type validation runs before str conversion                         #
# --------------------------------------------------------------------------- #


def test_real_leaf_rejects_dimension_mismatch():
    # A velocity-dimensioned quantity assigned to a pressure (Pa) leaf must be
    # rejected *before* it is rendered to a string.
    leaf = _FakeRealLeaf(units="Pa")
    velocity = Quantity(5.0, "m s^-1")
    with pytest.raises(TypeError, match="not compatible"):
        RealNumerical.set_state(leaf, velocity)
    assert leaf.captured is None  # never rendered / stored


def test_real_leaf_accepts_matching_dimension():
    leaf = _FakeRealLeaf(units="Pa")
    pressure_quantity = Quantity(101325.0, "Pa")
    RealNumerical.set_state(leaf, pressure_quantity)
    assert leaf.captured == "101325.0 [Pa]"


def test_real_leaf_rejects_vector_expression_kind(builder):
    # A scalar Real leaf does not accept a vector expression regardless of
    # dimensions.
    leaf = _FakeRealLeaf(units="m s^-1")
    vector = builder.vector.make_vec(
        x=builder.literal(1.0), y=builder.literal(2.0), z=builder.literal(3.0)
    )
    with pytest.raises(TypeError, match="kind 'vector'"):
        RealNumerical.set_state(leaf, vector)
    assert leaf.captured is None


def test_unknown_dimension_expression_is_not_blocked(pressure_expr):
    # A composite reduction reports no dimensions, so the dimensional check is
    # skipped and the expression is stored even against a differently-united
    # leaf (the kind check still passes: both scalar).
    assert pressure_expr.__settings_dimensions__() is None
    leaf = _FakeRealLeaf(units="m s^-1")
    RealNumerical.set_state(leaf, pressure_expr)
    assert leaf.captured == "AreaAve(AbsolutePressure,['inlet1'])"


# --------------------------------------------------------------------------- #
# List leaves render / validate each expression element                       #
# --------------------------------------------------------------------------- #


def test_real_list_renders_expression_elements(pressure_expr):
    # Each element of the list is rendered through the protocol; plain values
    # are left untouched and the list structure is preserved.
    leaf = _FakeRealListLeaf(units="Pa")
    RealNumerical.set_state(leaf, [1.0, pressure_expr, 3.0])
    assert leaf.captured == [1.0, "AreaAve(AbsolutePressure,['inlet1'])", 3.0]


def test_real_list_renders_settings_str_only_element():
    # An object implementing only ``__settings_str__`` is rendered via the
    # protocol rather than serialized with ``str()``.
    class _StrOnly:
        def __settings_str__(self):
            return "my_named_expression"

    leaf = _FakeRealListLeaf(units="Pa")
    RealNumerical.set_state(leaf, [_StrOnly()])
    assert leaf.captured == ["my_named_expression"]


def test_real_list_rejects_vector_element(builder):
    # Each element is validated with scalar kinds, so a vector element is
    # rejected even though the list leaf itself accepts a whole-list vector.
    leaf = _FakeRealListLeaf(units="m s^-1")
    vector = builder.vector.make_vec(
        x=builder.literal(1.0), y=builder.literal(2.0), z=builder.literal(3.0)
    )
    with pytest.raises(TypeError, match="kind 'vector'"):
        RealNumerical.set_state(leaf, [vector])
    assert leaf.captured is None


def test_real_list_rejects_dimension_mismatch_element():
    # A velocity-dimensioned element assigned to a pressure (Pa) list leaf is
    # rejected before any element is rendered.
    leaf = _FakeRealListLeaf(units="Pa")
    with pytest.raises(TypeError, match="not compatible"):
        RealNumerical.set_state(leaf, [Quantity(5.0, "m s^-1")])
    assert leaf.captured is None


def test_real_list_still_accepts_plain_list():
    leaf = _FakeRealListLeaf(units="Pa")
    RealNumerical.set_state(leaf, [1.0, 2.0, 3.0])
    assert leaf.captured == [1.0, 2.0, 3.0]


def test_render_list_helper_returns_none_without_expression_elements():
    leaf = _FakeRealListLeaf(units="Pa")
    # No expression element -> fall through to normal handling.
    assert _render_settings_expression_list(leaf, [1.0, 2.0], ("scalar",)) is None
    # A tuple is a (value, units) quantity, not an element container.
    assert _render_settings_expression_list(leaf, (1.0, "Pa"), ("scalar",)) is None


def test_real_list_resolves_leaf_units_once_per_assignment():
    # Each units() lookup is an uncached RPC on a real leaf. A list of
    # known-dimension expressions must resolve the leaf's units ONCE for the
    # whole assignment, not once per element.
    leaf = _FakeRealListLeaf(units="Pa")
    elements = [Quantity(float(i), "Pa") for i in range(5)]
    RealNumerical.set_state(leaf, elements)
    assert leaf.captured == [f"{float(i)} [Pa]" for i in range(5)]
    assert leaf.units_calls == 1


def test_real_list_mismatch_still_resolves_units_once():
    # A confident dimension mismatch is still raised, and only one units()
    # lookup is performed for the assignment.
    leaf = _FakeRealListLeaf(units="Pa")
    with pytest.raises(TypeError, match="not compatible"):
        RealNumerical.set_state(leaf, [Quantity(1.0, "Pa"), Quantity(2.0, "m s^-1")])
    assert leaf.units_calls == 1


# --------------------------------------------------------------------------- #
# _render_settings_expression contract                                        #
# --------------------------------------------------------------------------- #


def test_render_helper_returns_none_for_plain_value():
    leaf = _FakeRealLeaf()
    assert _render_settings_expression(leaf, 42.0) is None


def test_render_helper_validates_before_rendering():
    leaf = _FakeRealLeaf(units="Pa")
    velocity = Quantity(5.0, "m s^-1")
    with pytest.raises(TypeError):
        _render_settings_expression(leaf, velocity)


# --------------------------------------------------------------------------- #
# Parse a string, read its quantity type, compare with the target parameter   #
# --------------------------------------------------------------------------- #
#
# This mirrors the end-to-end flow a caller cares about: start from an
# expression *string*, parse it back into an expression object, ask that
# object for its quantity (structural) type, and check it against the quantity
# type the target settings parameter accepts -- all before any assignment.


@pytest.mark.parametrize(
    ("expression_string", "expected_kind"),
    [
        ("AreaAve(AbsolutePressure, ['inlet1'])", "scalar"),  # reduction -> scalar
        ("AbsolutePressure", "scalar"),  # bare variable -> scalar
        ("5 [m/s]", "quantity"),  # value-with-units -> quantity
        ("MakeVec(1, 2, 3)", "vector"),  # vector constructor -> vector
        ("AbsolutePressure > 0", "boolean"),  # comparison -> boolean
    ],
)
def test_parsed_expression_reports_its_quantity_type(
    builder, expression_string, expected_kind
):
    # Parse the string back into an expression object via the builder ...
    expr = builder.parse(expression_string)
    # ... and read the quantity (structural) type of the built object.
    assert expr.__settings_kind__() == expected_kind


@pytest.mark.parametrize(
    ("expression_string", "target_leaf_factory", "compatible"),
    [
        # A scalar expression is compatible with a scalar Real parameter.
        ("AreaAve(AbsolutePressure, ['inlet1'])", _FakeRealLeaf, True),
        # A value-with-units is also accepted by a Real parameter.
        ("101325 [Pa]", _FakeRealLeaf, True),
        # A vector expression is NOT compatible with a scalar Real parameter.
        ("MakeVec(1, 2, 3)", _FakeRealLeaf, False),
        # A boolean expression is NOT compatible with a scalar Real parameter.
        ("AbsolutePressure > 0", _FakeRealLeaf, False),
        # A vector expression IS compatible with a (string) definition
        # parameter, which accepts scalar/vector/boolean/quantity.
        ("MakeVec(1, 2, 3)", _FakeTextualLeaf, True),
    ],
)
def test_parsed_expression_kind_vs_target_parameter_kind(
    builder, expression_string, target_leaf_factory, compatible
):
    # Build the expression object from its string form.
    expr = builder.parse(expression_string)
    expr_kind = expr.__settings_kind__()

    # The "quantity type of the target parameter" is the set of kinds it
    # accepts, exposed via ``_expression_kinds``.
    target = target_leaf_factory()
    accepted_kinds = target._expression_kinds

    # Direct comparison of the two quantity types.
    assert (expr_kind in accepted_kinds) is compatible

    # And the settings layer enforces exactly this comparison before storing:
    if compatible:
        target.set_state_via(expr)  # stores the rendered string
        assert target.captured is not None
    else:
        with pytest.raises(TypeError, match=f"kind '{expr_kind}'"):
            target.set_state_via(expr)
        assert target.captured is None


# --------------------------------------------------------------------------- #
# SettingsBase enforces correct expression-protocol wiring at import time      #
# --------------------------------------------------------------------------- #
#
# Leaves declare ``SettingsBase`` before the behaviour mixin, so a bare
# ``set_state`` resolves to ``SettingsBase.set_state`` and silently bypasses the
# expression protocol. ``SettingsBase.__init_subclass__`` turns that easy-to-
# forget wiring mistake into a loud failure at class-definition time.


def test_guard_rejects_leaf_that_forgets_to_wire_set_state():
    # Declares _expression_kinds (opts in) but never wires an expression-aware
    # set_state -> set_state resolves to SettingsBase.set_state.
    with pytest.raises(TypeError, match="bypasses expression handling"):

        class _ForgotToWire(SettingsBase[str], Textual):
            _expression_kinds = ("scalar",)


def test_guard_rejects_leaf_that_forgets_base_set_state():
    # Routes set_state through an expression-aware setter but forgets to expose
    # the core setter as base_set_state (which that setter delegates to).
    with pytest.raises(TypeError, match="base_set_state"):

        class _HalfWired(SettingsBase[str], Textual):
            _expression_kinds = ("scalar",)
            set_state = Textual.set_state


def test_guard_accepts_correctly_wired_leaf():
    # A leaf that wires both set_state and base_set_state passes the guard.
    class _CorrectlyWired(SettingsBase[str], Textual):
        _expression_kinds = ("scalar",)
        base_set_state = SettingsBase[str].set_state
        set_state = Textual.set_state

    assert _CorrectlyWired.set_state is Textual.set_state
    assert _CorrectlyWired.base_set_state is SettingsBase.set_state


def test_guard_accepts_textual_list_setter():
    # The list helper used by StringList / FilenameList is a valid wiring too.
    class _CorrectlyWiredList(SettingsBase[list], Textual):
        _expression_kinds = ("scalar", "vector")
        base_set_state = SettingsBase[list].set_state
        set_state = _textual_list_set_state

    assert _CorrectlyWiredList.set_state is _textual_list_set_state
    assert _CorrectlyWiredList.base_set_state is SettingsBase.set_state


def test_guard_ignores_leaf_without_expression_kinds():
    # A leaf that does not opt into the protocol (no _expression_kinds anywhere
    # in its MRO) is unaffected, even though its set_state resolves to
    # SettingsBase.set_state.
    class _PlainLeaf(SettingsBase[int], Numerical):
        pass

    assert getattr(_PlainLeaf, "_expression_kinds", None) is None
    assert _PlainLeaf.set_state is SettingsBase.set_state  # no error raised


@pytest.mark.parametrize(
    "leaf_cls", [Real, RealList, String, StringList, Filename, FilenameList]
)
def test_shipped_expression_leaves_are_correctly_wired(leaf_cls):
    # Regression guard: every shipped leaf that opts into the protocol must not
    # resolve set_state back to the bypassing SettingsBase.set_state.
    assert leaf_cls._expression_kinds is not None
    assert leaf_cls.set_state is not SettingsBase.set_state
    assert leaf_cls.base_set_state is SettingsBase.set_state


# --------------------------------------------------------------------------- #
# Group dict updates and command arguments use the shared conversion path      #
# --------------------------------------------------------------------------- #
#
# Group dict updates (``named.set_state({'definition': obj})``) and command
# arguments both convert their values through ``to_scheme_keys`` -- NOT through
# the per-leaf ``set_state`` -- so the rendering/validation must live in that
# shared conversion path. ``SettingsBase.set_state`` forwards the result of
# ``to_scheme_keys`` straight to the backend, so asserting on ``to_scheme_keys``
# faithfully covers both flows.


def _group_with_child(child_cls, fluent_name="definition", python_name="definition"):
    """Build a minimal ``Group`` subclass exposing one leaf child."""

    child = type(f"_Child_{fluent_name}", (child_cls,), {"fluent_name": fluent_name})
    grp = type(
        "_Grp",
        (Group,),
        {
            "child_names": [python_name],
            "_child_classes": {python_name: child},
            "_child_aliases": {},
        },
    )
    return grp


def test_group_dict_update_renders_expression_value(pressure_expr):
    # A builder expression nested in a group dict is rendered to its string.
    grp = _group_with_child(String)
    out = grp.to_scheme_keys({"definition": pressure_expr}, grp, [])
    assert out == {"definition": "AreaAve(AbsolutePressure,['inlet1'])"}


def test_group_dict_update_renders_settings_str_only_value():
    # An object implementing only ``__settings_str__`` is rendered via the
    # protocol, not serialized with ``str()``.
    class _StrOnly:
        def __settings_str__(self):
            return "my_named_expression"

        def __repr__(self):
            return "<not the settings string>"

    grp = _group_with_child(String)
    out = grp.to_scheme_keys({"definition": _StrOnly()}, grp, [])
    assert out == {"definition": "my_named_expression"}


def test_group_dict_update_rejects_incompatible_kind(builder):
    # A String 'definition' child does not accept a location-list expression --
    # the kind check runs in the shared path too.
    grp = _group_with_child(String)
    location_list = builder.locations(["inlet1", "inlet2"])
    with pytest.raises(TypeError, match="kind 'location_list'"):
        grp.to_scheme_keys({"definition": location_list}, grp, [])


def test_group_dict_update_renders_real_list_elements(pressure_expr):
    # Nested real-list elements are rendered element-wise via the shared path.
    grp = _group_with_child(RealList, fluent_name="values", python_name="values")
    out = grp.to_scheme_keys({"values": [1.0, pressure_expr, 3.0]}, grp, [])
    assert out == {"values": [1.0, "AreaAve(AbsolutePressure,['inlet1'])", 3.0]}


def test_command_argument_renders_expression_value(pressure_expr):
    # Command arguments convert via ``<argument>.to_scheme_keys(...)`` -- the
    # same shared path -- so an expression argument is rendered, not str()'d.
    arg_cls = type("_ExprArg", (String,), {"fluent_name": "expression"})
    assert (
        arg_cls.to_scheme_keys(pressure_expr, arg_cls, [])
        == "AreaAve(AbsolutePressure,['inlet1'])"
    )


def test_command_argument_rejects_incompatible_kind(builder):
    # A Real-valued command argument rejects a vector expression before sending.
    arg_cls = type("_RealArg", (Real,), {"fluent_name": "value"})
    vector = builder.vector.make_vec(
        x=builder.literal(1.0), y=builder.literal(2.0), z=builder.literal(3.0)
    )
    with pytest.raises(TypeError, match="kind 'vector'"):
        arg_cls.to_scheme_keys(vector, arg_cls, [])


def test_read_case_data_filename_argument_renders_protocol_object(pressure_expr):
    # End-to-end command path: a Filename argument reaches ``before_execute``
    # (and ``expand_api_file_argument``) *before* ``to_scheme_keys``. A protocol
    # object must be normalized to its rendered string first, otherwise
    # ``value.replace(".cas", ".dat")`` raises ``AttributeError`` for
    # ``read_case_data``. The rendered value must also flow to ``after_execute``.
    from ansys.fluent.core.solver import flobject

    captured = {}

    class _CmdProxy:
        def get_static_info(self):
            return {
                "type": "group",
                "commands": {
                    "read-case-data": {
                        "type": "command",
                        "arguments": {
                            "file-name": {"type": "file", "file_purpose": "input"},
                        },
                    },
                },
            }

        def is_interactive_mode(self):
            return False

        def has_wildcard(self, name):
            return False

        def execute_cmd(self, parent_path, command, **kwds):
            captured["command"] = command
            captured["kwds"] = kwds
            return None

    root = flobject.get_root(_CmdProxy(), version="252")
    # Before the fix this raised AttributeError inside expand_api_file_argument.
    root.read_case_data.execute_command(file_name=pressure_expr)
    assert captured["command"] == "read-case-data"
    assert captured["kwds"] == {"file-name": "AreaAve(AbsolutePressure,['inlet1'])"}


def test_shared_path_passes_plain_values_through():
    # Non-expression values and non-opt-in leaves are untouched.
    assert _settings_expression_to_scheme(String, "plain string") == "plain string"
    assert _settings_expression_to_scheme(RealList, [1.0, 2.0]) == [1.0, 2.0]

    class _ExprOnly:
        def __settings_str__(self):
            return "x"

    # A leaf that does not opt into the protocol leaves the object untouched.
    obj = _ExprOnly()
    assert _settings_expression_to_scheme(Numerical, obj) is obj
