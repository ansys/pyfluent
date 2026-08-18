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

"""PyFluent Settings MCP Server.

Exposes the Fluent settings schema as five MCP tools so that LLMs can
explore, search, validate, and generate PyFluent scripts without a live
Fluent session.

Launch via stdio (for use with Claude Desktop, VS Code MCP, etc.)::

    python -m ansys.fluent.core._pf_mcp

or programmatically::

    import asyncio
    from ansys.fluent.core._pf_mcp import main
    asyncio.run(main())
"""

from __future__ import annotations

__all__ = ["main"]


def main() -> None:
    """Run the PyFluent Settings MCP server (stdio transport)."""
    import asyncio

    from .server import serve  # deferred so mcp is only required at run-time

    asyncio.run(serve())
