import os
import platform
import subprocess

from ansys.fluent.core.launcher import launcher
from ansys.fluent.core.utils.networking import find_remoting_ip


def get_subprocess_kwargs_for_fluent(env):
    print("Using custom get_subprocess_kwargs_for_fluent method")
    kwargs = {}
    # kwargs.update(stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if platform.system() == "Windows":
        kwargs.update(shell=True, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
    else:
        kwargs.update(shell=True, start_new_session=True)
    fluent_env = os.environ.copy()
    fluent_env.update({k: str(v) for k, v in env.items()})
    fluent_env["REMOTING_THROW_LAST_TUI_ERROR"] = "1"
    from ansys.fluent.core import INFER_REMOTING_IP

    if INFER_REMOTING_IP and not "REMOTING_SERVER_ADDRESS" in fluent_env:
        remoting_ip = find_remoting_ip()
        if remoting_ip:
            fluent_env["REMOTING_SERVER_ADDRESS"] = remoting_ip
    kwargs.update(env=fluent_env)
    return kwargs


launcher._get_subprocess_kwargs_for_fluent = get_subprocess_kwargs_for_fluent
