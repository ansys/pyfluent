"""Setup file for ansys-fluent-solver"""
import os
from setuptools import setup

# Get version from version info
__version__ = None
this_file = os.path.dirname(__file__)
version_file = os.path.join(this_file, "ansys", "fluent", "solver", "_version.py")
with open(version_file, mode="r") as fd:
    # execute file from raw string
    exec(fd.read())

install_requires = [
    'grpcio>=1.30.0',
    'ansys-api-fluent-v0>=0.0.1'
    ]

setup(
    name='ansys-fluent-solver',
    packages=['ansys.fluent.solver'],
    version=__version__,
    description="Fluent's SolverAPI exposed in Python",
    long_description=open('README.rst').read(),
    long_description_content_type='text/x-rst',
    url='https://github.com/mkundu1/pyfluent',
    license='MIT',
    author='ANSYS, Inc.',
    maintainer='Mainak Kundu',
    maintainer_email='mainak.kundu@ansys.com',
    install_requires=['grpcio>=1.30.0'],
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)