import os
import time

import ansys.fluent.core as pyfluent


def test_single_jou(with_launching_container):

    file_path = os.path.join(pyfluent.EXAMPLES_PATH, "jou1.jou")

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

    file_path = os.path.join(pyfluent.EXAMPLES_PATH, "jou1.scm")

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

    file_path_1 = os.path.join(pyfluent.EXAMPLES_PATH, "jou1.jou")
    file_path_2 = os.path.join(pyfluent.EXAMPLES_PATH, "jou2.jou")

    with open(file_path_1, "w") as journal:
        journal.write('(display "from jou1.jou")')

    with open(file_path_2, "w") as journal:
        journal.write('(display "from jou2.jou")')

    time.sleep(5)

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

    gen_file_name = file_path_1.rsplit("\\")[-1].split(".")[0] + '_' + file_path_2.rsplit("\\")[-1].split(".")[0] + '.py'  # noqa: E501

    gen_file_path = os.path.join(pyfluent.EXAMPLES_PATH, gen_file_name)
    print(gen_file_path)

    while os.path.exists(gen_file_path):
        try:
            os.remove(gen_file_path)
        except PermissionError:
            time.sleep(1)


def test_2_scm(with_launching_container):

    file_path_1 = os.path.join(pyfluent.EXAMPLES_PATH, "jou1.scm")
    file_path_2 = os.path.join(pyfluent.EXAMPLES_PATH, "jou2.scm")

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

    gen_file_name = file_path_1.rsplit("\\")[-1].split(".")[0] + '_' + file_path_2.rsplit("\\")[-1].split(".")[0] + '.py'  # noqa: E501

    gen_file_path = os.path.join(pyfluent.EXAMPLES_PATH, gen_file_name)
    print(gen_file_path)

    while os.path.exists(gen_file_path):
        try:
            os.remove(gen_file_path)
        except PermissionError:
            time.sleep(1)


if __name__ == "__main__":
    file_path_1 = os.path.join(pyfluent.EXAMPLES_PATH, "test_jou1.jou")
    file_path_2 = os.path.join(pyfluent.EXAMPLES_PATH, "test_jou2.jou")

    with open(file_path_1, "w") as journal:
        journal.write('(display "from jou1.jou")')

    with open(file_path_2, "w") as journal:
        journal.write('(display "from jou2.jou")')

    solver = pyfluent.launch_fluent(mode="solver", topy=[file_path_1, file_path_2])
    solver.exit()
