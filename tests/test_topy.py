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

import os
from pathlib import Path
import time

import pytest

import ansys.fluent.core as pyfluent


@pytest.mark.skip(reason="Unable to read generated python journal from fluent.")
def test_single_jou():
    file_name = os.path.join(pyfluent.config.examples_path, "jou1.jou")

    with open(file_name, "w") as journal:
        journal.write('(display "from jou1.jou")')

    solver = pyfluent.launch_fluent(mode="solver", topy=file_name)
    solver.exit()

    with open(file_name) as file:
        returned = file.readlines()

    if os.path.exists(file_name):
        os.remove(file_name)

    assert returned

    gen_file_name = os.path.join(os.getcwd(), f"{Path(file_name).stem}.py")

    with open(gen_file_name) as file:
        gen_returned = file.readlines()

    assert gen_returned

    while os.path.exists(gen_file_name):
        try:
            os.remove(gen_file_name)
        except PermissionError:
            time.sleep(1)
        if not os.path.exists(gen_file_name):
            break


@pytest.mark.skip(reason="Unable to read generated python journal from fluent.")
def test_single_scm():
    file_name = os.path.join(pyfluent.config.examples_path, "jou1.scm")

    with open(file_name, "w") as journal:
        journal.write('(display "from jou1.scm")')

    solver = pyfluent.launch_fluent(mode="solver", topy=file_name)
    solver.exit()

    with open(file_name) as file:
        returned = file.readlines()

    if os.path.exists(file_name):
        os.remove(file_name)

    assert returned

    gen_file_name = os.path.join(os.getcwd(), f"{Path(file_name).stem}.py")

    with open(gen_file_name) as file:
        gen_returned = file.readlines()

    assert gen_returned

    while os.path.exists(gen_file_name):
        try:
            os.remove(gen_file_name)
        except PermissionError:
            time.sleep(1)
        if not os.path.exists(gen_file_name):
            break


@pytest.mark.skip(reason="Unable to read generated python journal from fluent.")
def test_2_jou():
    file_name_1 = os.path.join(pyfluent.config.examples_path, "jou1.jou")
    file_name_2 = os.path.join(pyfluent.config.examples_path, "jou2.jou")

    with open(file_name_1, "w") as journal:
        journal.write('(display "from jou1.jou")')

    with open(file_name_2, "w") as journal:
        journal.write('(display "from jou2.jou")')

    solver = pyfluent.launch_fluent(mode="solver", topy=[file_name_1, file_name_2])
    solver.exit()

    with open(file_name_1) as file:
        returned1 = file.readlines()

    if os.path.exists(file_name_1):
        os.remove(file_name_1)

    assert returned1

    with open(file_name_2) as file:
        returned2 = file.readlines()

    if os.path.exists(file_name_2):
        os.remove(file_name_2)

    assert returned2

    gen_file_name = (
        Path(file_name_1).stem.split(".")[0]
        + "_"
        + Path(file_name_2).stem.split(".")[0]
        + ".py"
    )
    gen_file_name = os.path.join(os.getcwd(), gen_file_name)

    with open(gen_file_name) as file:
        gen_returned = file.readlines()

    assert gen_returned

    while os.path.exists(gen_file_name):
        try:
            os.remove(gen_file_name)
        except PermissionError:
            time.sleep(1)
        if not os.path.exists(gen_file_name):
            break


@pytest.mark.skip(reason="Unable to read generated python journal from fluent.")
def test_2_scm():
    file_name_1 = os.path.join(pyfluent.config.examples_path, "jou1.scm")
    file_name_2 = os.path.join(pyfluent.config.examples_path, "jou2.scm")

    with open(file_name_1, "w") as journal:
        journal.write('(display "from jou1.scm")')

    with open(file_name_2, "w") as journal:
        journal.write('(display "from jou2.scm")')

    solver = pyfluent.launch_fluent(mode="solver", topy=[file_name_1, file_name_2])
    solver.exit()

    with open(file_name_1) as file:
        returned1 = file.readlines()

    if os.path.exists(file_name_1):
        os.remove(file_name_1)

    assert returned1

    with open(file_name_2) as file:
        returned2 = file.readlines()

    if os.path.exists(file_name_2):
        os.remove(file_name_2)

    assert returned2

    gen_file_name = (
        Path(file_name_1).stem.split(".")[0]
        + "_"
        + Path(file_name_2).stem.split(".")[0]
        + ".py"
    )
    gen_file_name = os.path.join(os.getcwd(), gen_file_name)

    with open(gen_file_name) as file:
        gen_returned = file.readlines()

    assert gen_returned

    while os.path.exists(gen_file_name):
        try:
            os.remove(gen_file_name)
        except PermissionError:
            time.sleep(1)
        if not os.path.exists(gen_file_name):
            break
