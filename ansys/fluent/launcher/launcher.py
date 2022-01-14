import os
from pathlib import Path
import tempfile
import platform
import subprocess
import time
import yaml
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

from ansys.fluent.session import Session

THIS_DIR = os.path.dirname(__file__)
OPTIONS_FILE = os.path.join(THIS_DIR, 'launcher_options.yaml')
FLUENT_MAJOR_VERSION = '22'
FLUENT_MINOR_VERSION = '2'
LAUNCH_FLUENT_TIMEOUT = 100

def get_fluent_exe_path():
    exe_path = Path(os.getenv('AWP_ROOT' + FLUENT_MAJOR_VERSION + FLUENT_MINOR_VERSION))
    exe_path = exe_path / 'fluent'
    if platform.system() == 'Windows':
        exe_path = exe_path / 'ntbin' / 'win64' / 'fluent.exe'
    else:
        exe_path = exe_path / 'bin' / 'fluent'
    return str(exe_path)

def get_server_info_filepath():
    server_info_dir = os.getenv('SERVER_INFO_DIR')
    dir = Path(server_info_dir) if server_info_dir else Path.cwd()
    fd, filepath = tempfile.mkstemp(suffix='.txt', prefix='serverinfo-', dir=str(dir))
    os.close(fd)
    return filepath if server_info_dir else Path(filepath).name

def get_subprocess_kwargs_for_detached_process():
    kwargs = {}
    kwargs.update(stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if platform.system() == 'Windows':
        kwargs.update(creationflags=subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS) 
    else:
        kwargs.update(start_new_session=True)
    return kwargs

def launch_fluent(
    version = None,
    precision = None,
    processor_count = None,
    journal_filename = None
):
    """Start Fluent locally in server mode.
    Parameters
    ----------
    version : str, optional
        Whether to use the '2d' or '3d' version of Fluent. Default is '3d'.

    precision : str, optional
        Whether to use the single-precision or double-precision version of Fluent. Default is double-precision.

    processor_count : int, optional
        Specify number of processors. Default is 1.

    journal_filename : str, optional
        Read the specified journal file.

    Returns
    -------
    An instance of ansys.fluent.session.Session.
    """
    exe_path = get_fluent_exe_path()
    launch_string = exe_path
    argvals = locals()
    all_options = None
    with open(OPTIONS_FILE, 'r') as f:
        all_options = yaml.load(f, Loader)
    for k, v in all_options.items():
        argval = argvals.get(k, None)
        default = v.get('default', None)
        if argval is None and v.get('required', None) == True:
            argval = default
        if argval is not None:
            allowed_values = v.get('allowed_values', None)
            if allowed_values and argval not in allowed_values:
                if default is not None:
                    old_argval = argval
                    argval = default
                    print(f'Default value {argval} is chosen for {k} as the passed value '
                          f'{old_argval} is outside allowed_values {allowed_values}.')
                else:
                    print(f'{k} = {argval} is discarded '
                          f'as it is outside allowed_values {allowed_values}.')
                    continue
            fluent_values = v.get('fluent_values', None)
            if fluent_values:
                i = allowed_values.index(argval)
                argval = fluent_values[i]
            launch_string += v['fluent_format'].replace('{}', str(argval))
    server_info_filepath = get_server_info_filepath()
    try:
        launch_string += f' -sifile="{server_info_filepath}"'
        if not os.getenv('PYFLUENT_SHOW_SERVER_GUI'):
            launch_string += ' -hidden'
        print(f'Launching Fluent with cmd: {launch_string}')
        sifile_last_mtime = Path(server_info_filepath).stat().st_mtime
        kwargs = get_subprocess_kwargs_for_detached_process()
        subprocess.Popen(launch_string, **kwargs)
        counter = LAUNCH_FLUENT_TIMEOUT
        while True:
            if Path(server_info_filepath).stat().st_mtime > sifile_last_mtime:
                time.sleep(1)
                print('\nFluent process is successfully launched.')
                break
            if counter == 0:
                print('\nThe launch process has been timed out.')
                break
            time.sleep(1)
            counter -= 1
            print(f'Waiting for Fluent to launch...{counter:2} seconds remaining', end='\r')
        return Session(server_info_filepath)
    finally:
        Path(server_info_filepath).unlink(missing_ok=True)
