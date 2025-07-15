# Copyright (C) 2021 - 2025 ANSYS, Inc. and/or its affiliates.
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

"""Test Podman compose."""

import ansys.fluent.core as pyfluent
from ansys.fluent.core import examples
from ansys.fluent.core.utils.networking import get_free_port

port_1 = get_free_port()
port_2 = get_free_port()
container_dict = {"ports": {f"{port_1}": port_1, f"{port_2}": port_2}}

solver = pyfluent.launch_fluent(container_dict=container_dict, use_podman_compose=True)
assert len(solver._container.ports) == 2
case_file_name = examples.download_file("mixing_elbow.cas.h5", "pyfluent/mixing_elbow")
solver.file.read(file_name=case_file_name, file_type="case")
solver.exit()
