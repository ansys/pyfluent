"""Setup file for ansys-fluent-core."""
import os
import shutil

from setuptools import find_namespace_packages, setup

# Get version from version info
__version__ = None
_THIS_FILE = os.path.dirname(__file__)
_VERSION_FILE = os.path.join(
    _THIS_FILE, "src", "ansys", "fluent", "core", "_version.py"
)
with open(_VERSION_FILE, mode="r", encoding="utf8") as fd:
    # execute file from raw string
    exec(fd.read())

# Copy README.rst file to docs folder in ansys.fluent.core
_README_FILE = os.path.join(_THIS_FILE, "README.rst")
_DOCS_FILE = os.path.join(
    _THIS_FILE, "src", "ansys", "fluent", "core", "docs", "README.rst"
)
shutil.copy2(_README_FILE, _DOCS_FILE)

install_requires = [
    "ansys-api-fluent==0.3.5",
    "ansys-platform-instancemanagement~=1.0",
    "grpcio>=1.30.0",
    "numpy>=1.21.5",
    "appdirs>=1.4.0",
    "pandas>=1.1.5",
    "h5py>=3.7.0",
]


packages = []
for package in find_namespace_packages(where="src", include="ansys*"):
    if package.startswith("ansys.fluent"):
        packages.append(package)

setup(
    name="ansys-fluent-core",
    packages=packages,
    package_dir={"": "src"},
    include_package_data=True,
    version=__version__,
    description="Pythonic interface to Ansys Fluent",
    long_description=open(_README_FILE, encoding="utf8").read(),
    long_description_content_type="text/x-rst",
    license="MIT",
    author="ANSYS, Inc.",
    author_email="pyansys.support@ansys.com",
    maintainer="PyAnsys developers",
    maintainer_email="pyansys.maintainers@ansys.com",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    url="https://github.com/pyansys/pyfluent",
    python_requires=">=3.7",
    install_requires=install_requires,
)
