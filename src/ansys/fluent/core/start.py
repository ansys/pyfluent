"""Module containing the user-friendly prompt-based ``start()`` function"""

import json
import os

from ansys.fluent.core import connect_to_fluent, launch_fluent
from ansys.fluent.core.launcher.pyfluent_enums import LaunchMode

CONFIG_DIR = "fluent_configs"


def _prompt_user_for_options_standalone():
    precision = input("Enter precision (single/double, default: double): ") or "double"
    return {"precision": precision}


def _prompt_user_for_launch_options():
    options = (
        "Standalone: Fluent will start on this computer",
        "PIM: e.g., you are working in Ansys Lab or similar environment. Fluent will start in the cloud",
        "Container: a Docker image containing Fluent will start",
        "Slurm: you will configure Fluent to be queued on Slurm. You will have access to the session object before Fluent runs",
    )
    print("Select an option:")
    for idx, option_name in enumerate(options):
        print(f"{idx + 1}: {option_name}")
    option = ""
    while not (option.isdigit() and 1 <= int(option) <= len(options)):
        option = input("Select an option by number: ")
    option_name = options[int(option) - 1]
    print(f"Selecting option: {option_name}... ")
    if LaunchMode(int(option)) == LaunchMode.STANDALONE:
        return _prompt_user_for_options_standalone()


def _save_configuration(config_name, config):
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)
    config_path = os.path.join(CONFIG_DIR, f"{config_name}.json")
    with open(config_path, "w") as f:
        json.dump(config, f)


def _load_configuration(config_name):
    config_path = os.path.join(CONFIG_DIR, f"{config_name}.json")
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            return json.load(f)
    return None


def _list_configurations():
    if not os.path.exists(CONFIG_DIR):
        return []
    return [f.split(".")[0] for f in os.listdir(CONFIG_DIR) if f.endswith(".json")]


def _launch():
    configs = _list_configurations()
    if configs:
        print("Available configurations:")
        for idx, config_name in enumerate(configs):
            print(f"{idx + 1}: {config_name}")
        choice = input(
            "Select a configuration by number or press Enter to create a new one: "
        )
        if choice.isdigit() and 1 <= int(choice) <= len(configs):
            config_name = configs[int(choice) - 1]
            config = _load_configuration(config_name)
        else:
            config_name = input("Enter a name for the new configuration: ")
            config = _prompt_user_for_launch_options()
            save_config = input("Save this configuration? (y/n): ")
            if save_config.lower() == "y":
                _save_configuration(config_name, config)
    else:
        config_name = input("Enter a name for the new configuration: ")
        config = _prompt_user_for_launch_options()
        save_config = input("Save this configuration? (y/n): ")
        if save_config.lower() == "y":
            _save_configuration(config_name, config)

    session = launch_fluent(**config)
    print("Fluent launched successfully with the following configuration:")
    print(config)
    return session


def _prompt_user_for_connect_options():
    args = {}
    options = (
        "Specify a server info file path",
        "Specify server info data individually (or use defaults)",
    )
    print("Select an option:")
    for idx, option_name in enumerate(options):
        print(f"{idx + 1}: {option_name}")
    option = ""
    while not (option.isdigit() and 1 <= int(option) <= len(options)):
        option = input("Select an option by number: ")
    option_name = options[int(option) - 1]
    print(f"Selecting option: {option_name}... ")
    if int(option) == 1:
        args["server_info_file_name"] = input("Enter the server info file path: ")
    else:
        args["ip"] = (
            input("Enter an IP address or press Enter to use the current default: ")
            or None
        )
        args["port"] = (
            input("Enter a port number or press Enter to use the current default: ")
            or None
        )
        args["password"] = (
            input("Enter a password or press Enter if one is not required: ") or None
        )
        args["cleanup_on_exit"] = (
            input(
                "Shut down the connected Fluent session automatically when the PyFluent session exits? (y/n, default: n): "
            )
            or "n"
        ).lower() == "y"
        if args["cleanup_on_exit"]:
            args["start_watchdog"] = (
                input(
                    "Ensure that any local Fluent connections are properly closed (uses a separate watchdog process)? (y/n, default: y): "
                )
                or "y"
            ).lower() == "y"
        args["start_transcript"] = (
            input("Stream the Fluent transcript to PyFluent? (y/n, default: y): ")
            or "y"
        ).lower() == "y"
    return args


def _connect():
    config = _prompt_user_for_connect_options()
    session = connect_to_fluent(**config)
    return session


def start():
    """User-friendly, prompt-based function to start a PyFluent session"""
    # use enum here
    options = "Launch Fluent", "Connect to Fluent", "Just use PyFluent"
    print("Select an option:")
    for idx, option_name in enumerate(options):
        print(f"{idx + 1}: {option_name}")
    option = ""
    while not (option.isdigit() and 1 <= int(option) <= len(options)):
        option = input("Select an option by number: ")
    option_name = options[int(option) - 1]
    print(f"Selecting option: {option_name}... ")
    if int(option) == 1:
        return _launch()
    if int(option) == 2:
        return _connect()
