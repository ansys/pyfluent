"""Setup file for ansys-fluent-solver"""
import os
from setuptools import setup, find_namespace_packages

# Get version from version info
__version__ = None
THIS_FILE = os.path.dirname(__file__)
VERSION_FILE = os.path.join(
    THIS_FILE, "ansys", "fluent", "solver", "_version.py")
with open(VERSION_FILE, mode='r', encoding='utf8') as fd:
    # execute file from raw string
    exec(fd.read())

install_requires = [
    'grpcio>=1.30.0',
    #'ansys-api-fluent-v0>=0.0.1'
    ]

packages = []
for package in find_namespace_packages(include="ansys*"):
    if package.startswith("ansys.fluent"):
        packages.append(package)

setup(
    name='ansys-fluent-solver',
    packages=packages,
    version=__version__,
    description="Fluent's SolverAPI exposed in Python",
    long_description=open('README.rst', encoding='utf8').read(),
    long_description_content_type='text/x-rst',
    url='https://github.com/mkundu1/pyfluent',
    license='MIT',
    author='ANSYS, Inc.',
    maintainer='Mainak Kundu',
    maintainer_email='mainak.kundu@ansys.com',
    install_requires=install_requires,
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
