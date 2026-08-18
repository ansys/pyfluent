# Copyright (C) 2021 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Unit tests for the PyFluent MCP server tools.

All tests run against a synthetic mini-schema that mirrors the real schema
structure so no live Fluent session and no large JSON file is needed.
"""

from __future__ import annotations

import ast
import sys
import types as builtin_types

import pytest

# ---------------------------------------------------------------------------
# Synthetic schema fixture
# ---------------------------------------------------------------------------

_MINI_SCHEMA = {
    "type": "group",
    "help": "Root settings",
    "children": {
        "setup": {
            "type": "group",
            "help": "Setup settings",
            "api_exposure_level": "stable",
            "children": {
                "models": {
                    "type": "group",
                    "help": "Physics models",
                    "children": {
                        "energy": {
                            "type": "group",
                            "help": "Energy model settings",
                            "children": {
                                "enabled": {
                                    "type": "boolean",
                                    "help": "Enable energy equation",
                                    "api_exposure_level": "stable",
                                }
                            },
                            "commands": {},
                            "queries": {},
                        },
                        "viscous": {
                            "type": "group",
                            "help": "Viscous / turbulence model settings",
                            "children": {
                                "model": {
                                    "type": "string",
                                    "help": "Turbulence model name",
                                    "api_exposure_level": "stable",
                                }
                            },
                            "commands": {
                                "initialize": {
                                    "type": "command",
                                    "help": "Initialize the viscous model",
                                    "arguments": {},
                                }
                            },
                            "queries": {
                                "get_model_info": {
                                    "type": "query",
                                    "help": "Return info about current model",
                                    "arguments": {},
                                    "return_type": "string",
                                }
                            },
                        },
                    },
                    "commands": {},
                    "queries": {},
                },
                "materials": {
                    "type": "group",
                    "help": "Material definitions",
                    "children": {
                        "fluid": {
                            "type": "named-object",
                            "help": "Fluid material instances",
                            "object_type": {
                                "type": "group",
                                "help": "Fluid material properties",
                                "children": {
                                    "density": {
                                        "type": "real",
                                        "help": "Density in kg/m^3",
                                    },
                                    "viscosity": {
                                        "type": "real",
                                        "help": "Dynamic viscosity",
                                    },
                                },
                                "commands": {},
                                "queries": {},
                            },
                            "children": {},
                            "commands": {
                                "copy_by_name": {
                                    "type": "command",
                                    "help": "Copy material from database by name",
                                    "arguments": {
                                        "name": {
                                            "type": "string",
                                            "help": "Material name",
                                        },
                                    },
                                }
                            },
                            "queries": {},
                        }
                    },
                    "commands": {},
                    "queries": {},
                },
            },
            "commands": {},
            "queries": {},
        },
        "solution": {
            "type": "group",
            "help": "Solution controls",
            "children": {},
            "commands": {
                "initialize": {
                    "type": "command",
                    "help": "Initialize the solver",
                    "arguments": {},
                },
                "run_calculation": {
                    "type": "command",
                    "help": "Run solver iterations",
                    "arguments": {
                        "number_of_iterations": {
                            "type": "integer",
                            "help": "Number of iterations to run",
                        }
                    },
                },
            },
            "queries": {},
        },
    },
    "commands": {},
    "queries": {},
}


@pytest.fixture(autouse=True)
def patch_schema(monkeypatch, tmp_path):
    """Redirect schema_index to use the mini-schema instead of the 50 MB file."""
    import json

    import ansys.fluent.core._pf_mcp.schema_index as si

    schema_file = tmp_path / "fluent_settings_schema.json"
    schema_file.write_text(json.dumps(_MINI_SCHEMA), encoding="utf-8")

    monkeypatch.setattr(si, "SCHEMA_PATH", schema_file)
    monkeypatch.setattr(si, "_index", None)
    monkeypatch.setattr(si, "_keyword_index", None)

    yield

    # Reset global caches after each test
    si._index = None
    si._keyword_index = None


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _is_valid_python(code: str) -> bool:
    try:
        ast.parse(code)
        return True
    except SyntaxError:
        return False


# ---------------------------------------------------------------------------
# schema_index tests
# ---------------------------------------------------------------------------


class TestSchemaIndex:
    def test_root_is_indexed(self):
        from ansys.fluent.core._pf_mcp.schema_index import get_index

        idx = get_index()
        assert "" in idx
        assert idx[""].type == "group"

    def test_deep_path_indexed(self):
        from ansys.fluent.core._pf_mcp.schema_index import get_index

        idx = get_index()
        assert "setup.models.viscous.model" in idx
        assert idx["setup.models.viscous.model"].type == "string"

    def test_command_indexed(self):
        from ansys.fluent.core._pf_mcp.schema_index import get_index

        idx = get_index()
        assert "setup.models.viscous.initialize" in idx
        assert idx["setup.models.viscous.initialize"].type == "command"

    def test_query_indexed(self):
        from ansys.fluent.core._pf_mcp.schema_index import get_index

        idx = get_index()
        assert "setup.models.viscous.get_model_info" in idx
        assert idx["setup.models.viscous.get_model_info"].type == "query"

    def test_named_object_template_indexed(self):
        from ansys.fluent.core._pf_mcp.schema_index import get_index

        idx = get_index()
        assert "setup.materials.fluid[*]" in idx
        assert "setup.materials.fluid[*].density" in idx

    def test_canonicalize_instance_brackets(self):
        from ansys.fluent.core._pf_mcp.schema_index import canonicalize

        assert (
            canonicalize('setup.materials.fluid["air"].density')
            == "setup.materials.fluid[*].density"
        )
        assert (
            canonicalize("setup.materials.fluid['air'].density")
            == "setup.materials.fluid[*].density"
        )
        assert (
            canonicalize("setup.materials.fluid[0].density")
            == "setup.materials.fluid[*].density"
        )

    def test_keyword_index_populated(self):
        from ansys.fluent.core._pf_mcp.schema_index import get_keyword_index

        kw = get_keyword_index()
        # "viscous" appears in the path "setup.models.viscous"
        assert any("viscous" in p for p in kw.get("viscous", []))

    def test_valid_ops_command(self):
        from ansys.fluent.core._pf_mcp.schema_index import get_index

        idx = get_index()
        assert idx["setup.models.viscous.initialize"].valid_ops == ["command"]

    def test_valid_ops_query(self):
        from ansys.fluent.core._pf_mcp.schema_index import get_index

        idx = get_index()
        assert idx["setup.models.viscous.get_model_info"].valid_ops == ["query"]

    def test_valid_ops_settable(self):
        from ansys.fluent.core._pf_mcp.schema_index import get_index

        idx = get_index()
        ops = idx["setup.models.viscous.model"].valid_ops
        assert "get_state" in ops
        assert "set_state" in ops


# ---------------------------------------------------------------------------
# fluent_browse tests
# ---------------------------------------------------------------------------


class TestFluentBrowse:
    def test_root_returns_top_level_children(self):
        from ansys.fluent.core._pf_mcp.tools import fluent_browse

        result = fluent_browse("")
        assert "children" in result
        names = [c["name"] for c in result["children"]]
        assert "setup" in names
        assert "solution" in names

    def test_group_with_commands_and_queries(self):
        from ansys.fluent.core._pf_mcp.tools import fluent_browse

        result = fluent_browse("setup.models.viscous")
        assert "children" in result
        assert "commands" in result
        assert "queries" in result
        cmd_names = [c["name"] for c in result["commands"]]
        assert "initialize" in cmd_names

    def test_named_object_includes_template(self):
        from ansys.fluent.core._pf_mcp.tools import fluent_browse

        result = fluent_browse("setup.materials.fluid")
        assert result["type"] == "named-object"
        assert "instance_template" in result
        assert "density" in result["instance_template"]["children"]

    def test_invalid_path_returns_error_and_suggestions(self):
        from ansys.fluent.core._pf_mcp.tools import fluent_browse

        result = fluent_browse("setup.models.nonexistent")
        assert "error" in result
        assert "suggestions" in result

    def test_instance_bracket_path_normalised(self):
        from ansys.fluent.core._pf_mcp.tools import fluent_browse

        result = fluent_browse('setup.materials.fluid["air"]')
        assert "error" not in result
        assert result["type"] in ("group", "named-object", "list-object")


# ---------------------------------------------------------------------------
# fluent_info tests
# ---------------------------------------------------------------------------


class TestFluentInfo:
    def test_returns_node_details(self):
        from ansys.fluent.core._pf_mcp.tools import fluent_info

        result = fluent_info("setup.models.viscous.model")
        assert result["type"] == "string"
        assert "get_state" in result["valid_ops"]
        assert "set_state" in result["valid_ops"]

    def test_command_node_shows_arguments(self):
        from ansys.fluent.core._pf_mcp.tools import fluent_info

        result = fluent_info("solution.run_calculation")
        assert result["type"] == "command"
        assert "number_of_iterations" in result["arguments"]

    def test_query_node_shows_return_type(self):
        from ansys.fluent.core._pf_mcp.tools import fluent_info

        result = fluent_info("setup.models.viscous.get_model_info")
        assert result["type"] == "query"
        assert result.get("return_type") == "string"

    def test_invalid_path_returns_error(self):
        from ansys.fluent.core._pf_mcp.tools import fluent_info

        result = fluent_info("does.not.exist")
        assert "error" in result


# ---------------------------------------------------------------------------
# fluent_search tests
# ---------------------------------------------------------------------------


class TestFluentSearch:
    def test_finds_path_by_segment_name(self):
        from ansys.fluent.core._pf_mcp.tools import fluent_search

        results = fluent_search("viscous")
        paths = [r["path"] for r in results]
        assert any("viscous" in p for p in paths)

    def test_finds_by_help_text_word(self):
        from ansys.fluent.core._pf_mcp.tools import fluent_search

        results = fluent_search("turbulence")
        paths = [r["path"] for r in results]
        # "turbulence" appears in help text of setup.models.viscous
        assert any("viscous" in p for p in paths)

    def test_limit_respected(self):
        from ansys.fluent.core._pf_mcp.tools import fluent_search

        results = fluent_search("setup", limit=3)
        assert len(results) <= 3

    def test_returns_valid_ops(self):
        from ansys.fluent.core._pf_mcp.tools import fluent_search

        results = fluent_search("energy")
        for r in results:
            assert "valid_ops" in r

    def test_no_results_for_nonsense(self):
        from ansys.fluent.core._pf_mcp.tools import fluent_search

        results = fluent_search("xyzzy_nonexistent_term_abc123")
        assert isinstance(results, list)


# ---------------------------------------------------------------------------
# fluent_validate_path tests
# ---------------------------------------------------------------------------


class TestFluentValidatePath:
    def test_valid_path(self):
        from ansys.fluent.core._pf_mcp.tools import fluent_validate_path

        r = fluent_validate_path("setup.models.viscous.model")
        assert r["valid"] is True
        assert r["node_type"] == "string"

    def test_valid_instance_bracket_path(self):
        from ansys.fluent.core._pf_mcp.tools import fluent_validate_path

        r = fluent_validate_path('setup.materials.fluid["air"].density')
        assert r["valid"] is True
        assert r["canonical_path"] == "setup.materials.fluid[*].density"

    def test_invalid_path_with_suggestions(self):
        from ansys.fluent.core._pf_mcp.tools import fluent_validate_path

        r = fluent_validate_path("setup.models.viscous.typo")
        assert r["valid"] is False
        assert "suggestions" in r
        assert len(r["suggestions"]) > 0

    def test_command_path_valid(self):
        from ansys.fluent.core._pf_mcp.tools import fluent_validate_path

        r = fluent_validate_path("solution.run_calculation")
        assert r["valid"] is True
        assert r["valid_ops"] == ["command"]


# ---------------------------------------------------------------------------
# fluent_generate_script tests
# ---------------------------------------------------------------------------


class TestFluentGenerateScript:
    def test_set_state_generates_valid_python(self):
        from ansys.fluent.core._pf_mcp.tools import fluent_generate_script

        result = fluent_generate_script(
            [
                {
                    "path": "setup.models.viscous.model",
                    "op": "set_state",
                    "value": "k-omega-sst",
                },
            ]
        )
        assert result["validation_errors"] == []
        assert _is_valid_python(result["script"])
        assert "set_state('k-omega-sst')" in result["script"]

    def test_get_state_captures_result_var(self):
        from ansys.fluent.core._pf_mcp.tools import fluent_generate_script

        result = fluent_generate_script(
            [
                {
                    "path": "setup.models.energy.enabled",
                    "op": "get_state",
                    "result_var": "energy_enabled",
                },
            ]
        )
        assert result["validation_errors"] == []
        assert "energy_enabled = " in result["script"]

    def test_command_with_args(self):
        from ansys.fluent.core._pf_mcp.tools import fluent_generate_script

        result = fluent_generate_script(
            [
                {
                    "path": "solution.run_calculation",
                    "op": "command",
                    "args": {"number_of_iterations": 100},
                },
            ]
        )
        assert result["validation_errors"] == []
        assert _is_valid_python(result["script"])
        assert "number_of_iterations=100" in result["script"]

    def test_query_with_result_var(self):
        from ansys.fluent.core._pf_mcp.tools import fluent_generate_script

        result = fluent_generate_script(
            [
                {
                    "path": "setup.models.viscous.get_model_info",
                    "op": "query",
                    "result_var": "model_info",
                },
            ]
        )
        assert result["validation_errors"] == []
        assert "model_info = " in result["script"]

    def test_invalid_path_recorded_in_errors(self):
        from ansys.fluent.core._pf_mcp.tools import fluent_generate_script

        result = fluent_generate_script(
            [
                {"path": "setup.models.nonexistent", "op": "set_state", "value": 42},
            ]
        )
        assert len(result["validation_errors"]) == 1
        assert "not found" in result["validation_errors"][0]["error"]

    def test_set_state_on_command_is_error(self):
        from ansys.fluent.core._pf_mcp.tools import fluent_generate_script

        result = fluent_generate_script(
            [
                {"path": "solution.initialize", "op": "set_state", "value": "x"},
            ]
        )
        assert len(result["validation_errors"]) == 1

    def test_command_on_non_command_is_error(self):
        from ansys.fluent.core._pf_mcp.tools import fluent_generate_script

        result = fluent_generate_script(
            [
                {"path": "setup.models.viscous.model", "op": "command"},
            ]
        )
        assert len(result["validation_errors"]) == 1

    def test_include_launch_false(self):
        from ansys.fluent.core._pf_mcp.tools import fluent_generate_script

        result = fluent_generate_script(
            [{"path": "setup.models.energy.enabled", "op": "set_state", "value": True}],
            include_launch=False,
        )
        assert "launch_fluent" not in result["script"]
        assert "import ansys" not in result["script"]
        assert _is_valid_python(result["script"])

    def test_custom_session_var(self):
        from ansys.fluent.core._pf_mcp.tools import fluent_generate_script

        result = fluent_generate_script(
            [{"path": "setup.models.energy.enabled", "op": "set_state", "value": True}],
            session_var="session",
        )
        assert "session.settings" in result["script"]

    def test_instance_bracket_in_path_preserved(self):
        from ansys.fluent.core._pf_mcp.tools import fluent_generate_script

        result = fluent_generate_script(
            [
                {
                    "path": 'setup.materials.fluid["air"].density',
                    "op": "set_state",
                    "value": 1.225,
                },
            ]
        )
        assert result["validation_errors"] == []
        # bracket notation preserved in generated code
        assert 'fluid["air"].density' in result["script"]

    def test_multi_op_script_valid_python(self):
        from ansys.fluent.core._pf_mcp.tools import fluent_generate_script

        result = fluent_generate_script(
            [
                {
                    "path": "setup.models.energy.enabled",
                    "op": "set_state",
                    "value": True,
                    "comment": "Turn on energy equation",
                },
                {
                    "path": "setup.models.viscous.model",
                    "op": "set_state",
                    "value": "k-omega-sst",
                },
                {
                    "path": "setup.models.viscous.model",
                    "op": "get_state",
                    "result_var": "current_model",
                },
                {
                    "path": "solution.run_calculation",
                    "op": "command",
                    "args": {"number_of_iterations": 200},
                },
            ]
        )
        assert result["validation_errors"] == []
        assert _is_valid_python(result["script"])

    def test_boolean_value_formatted_correctly(self):
        from ansys.fluent.core._pf_mcp.tools import fluent_generate_script

        result = fluent_generate_script(
            [
                {
                    "path": "setup.models.energy.enabled",
                    "op": "set_state",
                    "value": True,
                },
            ]
        )
        assert "set_state(True)" in result["script"]

    def test_dict_value_formatted_correctly(self):
        from ansys.fluent.core._pf_mcp.tools import fluent_generate_script

        result = fluent_generate_script(
            [
                {
                    "path": "setup.models.viscous",
                    "op": "set_state",
                    "value": {"model": "laminar"},
                },
            ]
        )
        assert result["validation_errors"] == []
        assert "{'model': 'laminar'}" in result["script"]

    def test_comment_appears_in_script(self):
        from ansys.fluent.core._pf_mcp.tools import fluent_generate_script

        result = fluent_generate_script(
            [
                {
                    "path": "setup.models.energy.enabled",
                    "op": "set_state",
                    "value": True,
                    "comment": "Enable heat transfer",
                },
            ]
        )
        assert "# Enable heat transfer" in result["script"]
