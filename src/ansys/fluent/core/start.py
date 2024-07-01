"""Module containing the user-friendly prompt-based ``start()`` function"""

import json
import os

from ansys.fluent.core import launch_fluent

CONFIG_DIR = "fluent_configs"


def _prompt_user_for_options():
    # Example prompt for simplicity
    # version = input("Enter Fluent version (default: latest): ") or "latest"
    precision = input("Enter precision (single/double, default: double): ") or "double"
    return {
        #    "version": version,
        "precision": precision
    }


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
            config = _prompt_user_for_options()
            save_config = input("Save this configuration? (y/n): ")
            if save_config.lower() == "y":
                _save_configuration(config_name, config)
    else:
        config_name = input("Enter a name for the new configuration: ")
        config = _prompt_user_for_options()
        save_config = input("Save this configuration? (y/n): ")
        if save_config.lower() == "y":
            _save_configuration(config_name, config)

    solver = launch_fluent(**config)
    print("Fluent launched successfully with the following configuration:")
    print(config)
    return solver


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
    print(f"Selecting option: {option_name}...")
    if int(option) == 1:
        return _launch()
