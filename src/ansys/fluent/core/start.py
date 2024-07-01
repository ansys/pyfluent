"""Module containing the user-friendly prompt-based ``start()`` function"""

from enum import Enum
import inspect
import json
import os
from typing import _UnionGenericAlias

from ansys.fluent.core import connect_to_fluent, launch_fluent
from ansys.fluent.core.launcher.launcher import mode_to_launcher_type
from ansys.fluent.core.launcher.pyfluent_enums import LaunchMode

CONFIG_DIR = "fluent_configs"


def _prompt_user_for_options_in_launch_mode(launch_mode):
    launcher_type = mode_to_launcher_type(launch_mode)
    init_method = launcher_type.__init__
    launcher_type_args = inspect.signature(init_method).parameters
    init_doc_list = inspect.getdoc(init_method).split("\n")
    params_pos = init_doc_list.index("Parameters")
    returns_pos = init_doc_list.index("Returns")
    init_doc_list = init_doc_list[params_pos + 1 : returns_pos]

    def print_arg(name, defn):
        def get_annotation(arg_defn):
            annotation = arg_defn.annotation
            if not isinstance(annotation, _UnionGenericAlias):
                return annotation
            return f"Union{[x.__name__ for x in annotation.__args__]}"

        if name != "self":
            print(f"{name} : {get_annotation(defn)}, default : {defn.default}")

    def print_launcher_arg_list():
        print(
            f"The following arguments apply to {launcher_type.__name__} ({inspect.getdoc(launcher_type)})...\n"
        )
        for name, defn in launcher_type_args.items():
            print_arg(name, defn)

    print_launcher_arg_list()
    arg_vals = {}
    while True:
        arg_name = input(
            "\nEnter 'list' for the argument list,"
            " press Enter to launch without making further changes,"
            " or enter an argument name to change its value: "
        )
        if not arg_name:
            break
        if arg_name.lower() in ("list", "'list'"):
            print_launcher_arg_list()
        elif arg_name != "self" and arg_name in launcher_type_args:
            print_arg(arg_name, launcher_type_args[arg_name])
            found_name = False
            for line in init_doc_list:
                if found_name:
                    if line.startswith(" "):
                        print(line.strip())
                    else:
                        break
                else:
                    found_name = line.startswith(arg_name + " ")
                    if found_name:
                        print(f"Detailed documentation for {line.strip()}:")
            value = (
                input(
                    f"\nEnter a value for {arg_name} or press Enter to keep the default: "
                )
                or None
            )
            if value is not None:
                import ansys  # noqa: F401

                arg_vals[arg_name] = eval(value)
    return arg_vals


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
    print(f"Selecting option: {option_name}...\n")
    return _prompt_user_for_options_in_launch_mode(LaunchMode(int(option)))


def _save_configuration(config_name, config_in):
    config = {}
    for k, v in config.items():
        if isinstance(v, Enum):
            value_of_enum = v.value
            if isinstance(value_of_enum, tuple):
                config[k] = value_of_enum[0]
            else:
                config[k] = value_of_enum
        else:
            config[k] = v
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


def _launch_for_config(config):
    session = launch_fluent(**config)
    print("Fluent launched successfully with the following configuration:")
    print(config)
    return session


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
            save_config = input("\nSave this configuration? (y/n): ")
            if save_config.lower() == "y":
                _save_configuration(config_name, config)
    else:
        config_name = input("Enter a name for the new configuration: ")
        config = _prompt_user_for_launch_options()
        save_config = input("\nSave this configuration? (y/n): ")
        if save_config.lower() == "y":
            _save_configuration(config_name, config)
    _launch_for_config(config)


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


def _start():
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


def start(config_name: dict = None):
    """User-friendly, prompt-based function to start a PyFluent session"""
    if config_name:
        return _launch_for_config(_load_configuration(config_name))
    else:
        return _start()
