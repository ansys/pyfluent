import os
import tempfile
import time

import ansys.fluent.core as pyfluent


def test_single_jou(with_launching_container):

    fd, file_path = tempfile.mkstemp(
        suffix=f"-{os.getpid()}.jou",
        prefix="jou1-",
        dir=str(pyfluent.EXAMPLES_PATH),
    )
    os.close(fd)

    with open(file_path, "w") as journal:
        journal.write('(display "from jou1.jou")')

    solver = pyfluent.launch_fluent(mode="solver", topy=file_path)
    solver.exit()

    with open(file_path) as file:
        returned = file.readlines()

    if os.path.exists(file_path):
        os.remove(file_path)

    assert returned

    gen_file_path = f'{file_path.split(".")[0]}.py'

    with open(gen_file_path) as file:
        gen_returned = file.readlines()

    assert gen_returned

    while os.path.exists(gen_file_path):
        try:
            os.remove(gen_file_path)
        except PermissionError:
            time.sleep(1)


def test_single_scm(with_launching_container):

    fd, file_path = tempfile.mkstemp(
        suffix=f"-{os.getpid()}.scm",
        prefix="jou1-",
        dir=str(pyfluent.EXAMPLES_PATH),
    )
    os.close(fd)

    with open(file_path, "w") as journal:
        journal.write('(display "from jou1.scm")')

    solver = pyfluent.launch_fluent(mode="solver", topy=file_path)
    solver.exit()

    with open(file_path) as file:
        returned = file.readlines()

    if os.path.exists(file_path):
        os.remove(file_path)

    assert returned

    gen_file_path = f'{file_path.split(".")[0]}.py'

    with open(gen_file_path) as file:
        gen_returned = file.readlines()

    assert gen_returned

    while os.path.exists(gen_file_path):
        try:
            os.remove(gen_file_path)
        except PermissionError:
            time.sleep(1)


def test_2_jou(with_launching_container):

    fd, file_path_1 = tempfile.mkstemp(
        suffix=f"-{os.getpid()}.jou",
        prefix="jou1-",
        dir=str(pyfluent.EXAMPLES_PATH),
    )
    os.close(fd)

    fd, file_path_2 = tempfile.mkstemp(
        suffix=f"-{os.getpid()}.jou",
        prefix="jou2-",
        dir=str(pyfluent.EXAMPLES_PATH),
    )
    os.close(fd)

    with open(file_path_1, "w") as journal:
        journal.write('(display "from jou1.jou")')

    with open(file_path_2, "w") as journal:
        journal.write('(display "from jou2.jou")')

    solver = pyfluent.launch_fluent(mode="solver", topy=[file_path_1, file_path_2])
    solver.exit()

    with open(file_path_1) as file:
        returned1 = file.readlines()

    if os.path.exists(file_path_1):
        os.remove(file_path_1)

    assert returned1

    with open(file_path_2) as file:
        returned2 = file.readlines()

    if os.path.exists(file_path_2):
        os.remove(file_path_2)

    assert returned2

    gen_file_path = f'{file_path_1.split(".")[0]}_{file_path_1.split(".")[0]}.py'

    while os.path.exists(gen_file_path):
        try:
            os.remove(gen_file_path)
        except PermissionError:
            time.sleep(1)


def test_2_scm(with_launching_container):

    fd, file_path_1 = tempfile.mkstemp(
        suffix=f"-{os.getpid()}.scm",
        prefix="jou1-",
        dir=str(pyfluent.EXAMPLES_PATH),
    )
    os.close(fd)

    fd, file_path_2 = tempfile.mkstemp(
        suffix=f"-{os.getpid()}.scm",
        prefix="jou2-",
        dir=str(pyfluent.EXAMPLES_PATH),
    )
    os.close(fd)

    with open(file_path_1, "w") as journal:
        journal.write('(display "from jou1.scm")')

    with open(file_path_2, "w") as journal:
        journal.write('(display "from jou2.scm")')

    solver = pyfluent.launch_fluent(mode="solver", topy=[file_path_1, file_path_2])
    solver.exit()

    with open(file_path_1) as file:
        returned1 = file.readlines()

    if os.path.exists(file_path_1):
        os.remove(file_path_1)

    assert returned1

    with open(file_path_2) as file:
        returned2 = file.readlines()

    if os.path.exists(file_path_2):
        os.remove(file_path_2)

    assert returned2

    gen_file_path = f'{file_path_1.split(".")[0]}_{file_path_1.split(".")[0]}.py'

    while os.path.exists(gen_file_path):
        try:
            os.remove(gen_file_path)
        except PermissionError:
            time.sleep(1)
