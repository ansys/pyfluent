# Copyright (C) 2021 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT
#
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

"""This module contains the code generation logic for Fluent's Python API."""

from enum import Enum, auto
from pathlib import Path


def get_codegen_version_dir(version: str | None = None, outdir: Path | None = None) -> Path:
    """Return the generated code directory for a specific Fluent version.

    The output tree is organized as ``<CODEGEN_OUTDIR>/vNNN/...`` so that older
    generated versions can be removed as a single unit during packaging.
    """
    from ansys.fluent.core.module_config import config

    base_dir = Path(outdir) if outdir is not None else Path(config.codegen_outdir)
    if version is None:
        return base_dir.resolve()
    normalized = "".join(str(version).split("."))
    return (base_dir / f"v{normalized}").resolve()


class StaticInfoType(Enum):
    """An enumeration over the different types of static info that can be fetched from
    Fluent."""

    TUI_SOLVER = auto()
    TUI_MESHING = auto()
    DATAMODEL_WORKFLOW = auto()
    DATAMODEL_MESHING_WORKFLOW = auto()
    DATAMODEL_MESHING = auto()
    DATAMODEL_PART_MANAGEMENT = auto()
    DATAMODEL_PM_FILE_MANAGEMENT = auto()
    DATAMODEL_FLICING = auto()
    DATAMODEL_PREFERENCES = auto()
    DATAMODEL_SOLVER_WORKFLOW = auto()
    DATAMODEL_MESHING_UTILITIES = auto()
    SETTINGS = auto()
