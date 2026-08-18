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

"""MCP server wiring for the PyFluent settings tools.

Transport: stdio (compatible with Claude Desktop, VS Code MCP, and any
MCP-aware LLM client).

Exposed tools
-------------
fluent_browse          – explore tree at a path
fluent_info            – full schema detail for one node
fluent_search          – keyword search across paths and help text
fluent_validate_path   – check a path exists in the schema
fluent_generate_script – emit a complete, validated PyFluent script
"""

from __future__ import annotations

import json
from typing import Any

from mcp.server import MCPServer

from .tools import (
    fluent_browse,
    fluent_generate_script,
    fluent_info,
    fluent_search,
    fluent_validate_path,
)

_server = MCPServer("pyfluent-settings-mcp")

# ---------------------------------------------------------------------------
# Tool handlers  (MCPServer infers JSON schema from type annotations)
# ---------------------------------------------------------------------------

_BROWSE_DESC = (
    "Explore the Fluent settings tree at a given dot-path. "
    "Returns node type, help text, children, commands, and queries at that location. "
    "Use '' (empty string) to list the top-level settings groups (setup, solution, …). "
    "For named-object nodes (materials, boundary conditions) the instance access "
    "pattern and instance template structure are also returned. "
    "Example paths: '', 'setup', 'setup.models', 'setup.materials.fluid[*]'."
)

_INFO_DESC = (
    "Get full schema details for one Fluent settings path: node type, help text, "
    "children / command / query names, argument types, valid operations "
    "(get_state / set_state / command / query), and API exposure level. "
    "Always call this before generating set_state or command calls to verify "
    "argument names and types. "
    "Examples: 'setup.models.viscous.model', 'setup.materials.database.copy_by_name'."
)

_SEARCH_DESC = (
    "Search for Fluent settings, commands, or queries by keyword. "
    "Searches both path segment names and help text; returns a ranked list of "
    "matching paths with type and description. "
    "Use when you do not know the exact path. "
    "Example keywords: 'viscous', 'turbulence', 'boundary condition', 'energy'."
)

_VALIDATE_DESC = (
    "Check whether a dot-path exists in the Fluent settings schema. "
    'Instance brackets such as ["air"] or [0] are normalised to [*] before lookup. '
    "Returns valid/invalid status, canonical form, node type, valid operations, "
    "and nearby suggestions when the path is invalid."
)

_GENERATE_DESC = (
    "Generate a complete, runnable PyFluent Python script from an ordered list of "
    "operations. Every path is validated against the schema; invalid paths produce "
    "an error comment in the script and appear in validation_errors. "
    "Supported ops: 'get_state', 'set_state', 'command', 'query'.\n\n"
    "Recommended workflow:\n"
    "  1. fluent_search        → find candidate paths\n"
    "  2. fluent_browse        → explore children / commands\n"
    "  3. fluent_info          → confirm argument names and types\n"
    "  4. fluent_validate_path → final path check\n"
    "  5. fluent_generate_script → emit the script\n\n"
    "Each operation dict must have 'path' and 'op' keys. Optional keys:\n"
    "  'value'      – value to set (set_state)\n"
    "  'args'       – keyword arguments dict (command / query)\n"
    "  'result_var' – variable name to capture get_state / query result\n"
    "  'comment'    – comment line emitted above the operation in the script"
)


@_server.tool(name="fluent_browse", description=_BROWSE_DESC)
def _browse(path: str = "") -> str:
    return json.dumps(fluent_browse(path), indent=2)


@_server.tool(name="fluent_info", description=_INFO_DESC)
def _info(path: str) -> str:
    return json.dumps(fluent_info(path), indent=2)


@_server.tool(name="fluent_search", description=_SEARCH_DESC)
def _search(keyword: str, limit: int = 20) -> str:
    return json.dumps(fluent_search(keyword, limit), indent=2)


@_server.tool(name="fluent_validate_path", description=_VALIDATE_DESC)
def _validate(path: str) -> str:
    return json.dumps(fluent_validate_path(path), indent=2)


@_server.tool(name="fluent_generate_script", description=_GENERATE_DESC)
def _generate(
    operations: list[Any],
    session_var: str = "solver",
    include_launch: bool = True,
) -> str:
    return json.dumps(
        fluent_generate_script(
            operations=operations,
            session_var=session_var,
            include_launch=include_launch,
        ),
        indent=2,
    )


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


async def serve() -> None:
    """Run the MCP server over stdio."""
    await _server.run_stdio_async()
