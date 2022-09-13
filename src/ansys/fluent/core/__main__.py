import sys
import os

from ansys.fluent.core.session_solver import Solver
from ansys.fluent.core.launcher.launcher import launch_fluent

def setup_for_fluent(version: str, mode: str):
    """Uses global PyConsole objects"""
    session = launch_fluent(version=version, mode=mode)
    if mode == 'meshing':
        globals()['meshing'] = session
        globals()['workflow'] = session.workflow
        globals()['solver'] = Solver(fluent_connection=session.fluent_connection)
    elif mode == 'solver':
        globals()['solver'] = session

# File name parsing from command line arguments
if len(sys.argv) > 1:
    file_path = ''
    for arg in sys.argv[1:]:
        if type(arg) == str and arg.endswith('.py') and os.path.exists(arg):
            file_path = arg
            break
    if file_path != '':
        with open(file_path, 'r') as filename:
            for line in filename.readlines():
                exec(line)

