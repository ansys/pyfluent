# Copyright (C) 2021 - 2026 ANSYS, Inc. and/or its affiliates.
# Copyright (C) 2023 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT
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

"""Launch and configure Fluent in Docker or Podman containers.

The package provides :class:`ComposeBasedLauncher` for launching Fluent with
Docker Compose or Podman Compose, together with utilities for selecting Fluent
container images and configuring gRPC launcher arguments in GitHub Actions.
"""

from .docker_compose import ComposeBasedLauncher
from .utils import get_ghcr_fluent_image_name, get_grpc_launcher_args_for_gh_runs

__all__ = [
    "ComposeBasedLauncher",
    "get_ghcr_fluent_image_name",
    "get_grpc_launcher_args_for_gh_runs",
]
