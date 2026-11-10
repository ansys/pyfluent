# Copyright (C) 2021 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT

"""Guard: the generic expression package must stay product-agnostic.

``ansys.fluent.core.offline.expressions._generic`` is intended to move to the
``ansys-units`` distribution, so it must not import, or mention, any product.
"""

import ast
from pathlib import Path

import pytest

import ansys.fluent.core.offline.expressions._generic as generic

_GENERIC_DIR = Path(generic.__file__).parent
_SOURCES = sorted(_GENERIC_DIR.glob("*.py"))
_ALLOWED_ABSOLUTE_IMPORTS = ("ansys.units",)


@pytest.mark.parametrize("source", _SOURCES, ids=lambda p: p.name)
def test_generic_imports_are_product_agnostic(source: Path):
    tree = ast.parse(source.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            if node.level > 1:
                pytest.fail(
                    f"{source.name}: imports outside the package ({node.module})"
                )
            if node.level == 0:
                modules = [node.module or ""]
            else:
                continue
        elif isinstance(node, ast.Import):
            modules = [alias.name for alias in node.names]
        else:
            continue
        for module in modules:
            if module.startswith("ansys.") and not module.startswith(
                _ALLOWED_ABSOLUTE_IMPORTS
            ):
                pytest.fail(f"{source.name}: imports product module {module!r}")


@pytest.mark.parametrize("source", _SOURCES, ids=lambda p: p.name)
def test_generic_sources_do_not_mention_products(source: Path):
    assert "fluent" not in source.read_text(encoding="utf-8").lower()
