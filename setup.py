"""Setup file for ansys-fluent-solver"""
import os
from setuptools import setup

THIS_PATH = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(THIS_PATH, "version.txt"), "r") as f:
    version = f.readline()

setup(
    name='ansys-fluent-solver',
    packages=['ansys.fluent.solver'],
    version=version,
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