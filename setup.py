"""Setup file for ansys-fluent-solver"""
import os

from setuptools import find_namespace_packages, setup

# Get version from version info
__version__ = None
_THIS_FILE = os.path.dirname(__file__)
_VERSION_FILE = os.path.join(
    _THIS_FILE, "ansys", "fluent", "core", "_version.py"
)
with open(_VERSION_FILE, mode="r", encoding="utf8") as fd:
    # execute file from raw string
    exec(fd.read())

install_requires = [
    "grpcio>=1.30.0",
    "numpy>=1.21.5",
    "protobuf>=3.12.2",
]

install_requires_post = [
    "vtk==9.1.0",
    "pyvista==0.33.2",
    "pyvistaqt==0.7.0",
    "pyside6==6.2.3",
    "matplotlib==3.5.1",
]

packages = []
for package in find_namespace_packages(include="ansys*"):
    if package.startswith("ansys.api"):
        packages.append(package)
    if package.startswith("ansys.fluent"):
        packages.append(package)

setup(
    name="ansys-fluent-solver",
    packages=packages,
    include_package_data=True,
    version=__version__,
    description="Pythonic interface to Ansys Fluent",
    long_description=open("README.rst", encoding="utf8").read(),
    long_description_content_type="text/x-rst",
    url="https://github.com/pyansys/pyfluent",
    license="MIT",
    author="ANSYS, Inc.",
    maintainer="Mainak Kundu",
    maintainer_email="mainak.kundu@ansys.com",
    install_requires=install_requires,
    extras_require={
        "post": install_requires_post,
    },
    python_requires=">3.6",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
