# Copyright (C) 2021 - 2026 ANSYS, Inc. and/or its affiliates.
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

"""Backward-compatibility shim for app_utilities (v0 proto API).

New code should import from:
* :mod:`ansys.fluent.core.services.app_utilities_v0` — gRPC service stubs
* :mod:`ansys.fluent.core.application_runtime` — business-logic wrappers
"""

from ansys.fluent.core.application_runtime import (
    ApplicationRuntimeOld as AppUtilitiesOld,
)
from ansys.fluent.core.application_runtime import (
    ApplicationRuntimeV252 as AppUtilitiesV252,
)
from ansys.fluent.core.application_runtime import (
    BuildInfo,
    ProcessInfo,
)

# Re-export data classes and business-logic wrappers under their old names
from ansys.fluent.core.application_runtime import (  # noqa: F401
    ApplicationRuntime as AppUtilities,
)

# Re-export gRPC service stub
from ansys.fluent.core.services.app_utilities_v0 import (  # noqa: F401
    AppUtilitiesService,
)
