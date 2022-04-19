"""Setup file for ansys-fluent-solver"""
import os
import platform
import struct
import sys

from setuptools import find_namespace_packages, setup

# Get version from version info
__version__ = None
THIS_FILE = os.path.dirname(__file__)
VERSION_FILE = os.path.join(
    THIS_FILE, "ansys", "fluent", "core", "_version.py"
)
with open(VERSION_FILE, mode="r", encoding="utf8") as fd:
    # execute file from raw string
    exec(fd.read())

install_requires = [
    "grpcio>=1.30.0",
    "numpy>=1.21.5",
    "pyvista>=0.33.2",
    "protobuf>=3.12.2",
    "pyvistaqt>=0.7.0",
    "PySide6>=6.2.3",
]

is64 = struct.calcsize("P") * 8 == 64
if sys.version_info.minor == 10 and is64:
    if platform.system().lower() == "linux":
        install_requires.append(
            "vtk @ https://github.com/pyvista/pyvista-wheels/raw/main/vtk-9.1.0.dev0-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl" # noqa: E501
        )
    elif platform.system().lower() == "windows":
        install_requires.append(
            "vtk @ https://github.com/pyvista/pyvista-wheels/raw/main/vtk-9.1.0.dev0-cp310-cp310-win_amd64.whl" # noqa: E501
        )

packages = []
for package in find_namespace_packages(include="ansys*"):
    if package.startswith("ansys.api"):
        packages.append(package)
    if package.startswith("ansys.fluent"):
        packages.append(package)

setup(
    name="ansys-fluent-solver",
    packages=packages,
    data_files=[("/ansys/fluent/",["README.rst"])],
    include_package_data=True,
    version=__version__,
    description="Fluent's SolverAPI exposed in Python",
    long_description=open("README.rst", encoding="utf8").read(),
    long_description_content_type="text/x-rst",
    url="https://github.com/pyansys/pyfluent",
    license="MIT",
    author="ANSYS, Inc.",
    maintainer="Mainak Kundu",
    maintainer_email="mainak.kundu@ansys.com",
    install_requires=install_requires,
    python_requires=">3.6",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
