"""Common public type aliases for PyFluent.

This module centralizes reusable typing constructs so that they can be
imported internally and are also exposed as part of the public API.
"""

from __future__ import annotations

import os
from typing import TypeAlias

PathType: TypeAlias = "os.PathLike[str | bytes] | str | bytes"
"""Type alias for file system paths."""
