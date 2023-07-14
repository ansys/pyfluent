"""Module controlling PyFluent's logging functionality."""
import logging.config
import os
from typing import Union

import yaml

_logging_file_enabled = False


def root_config():
    """Sets up the root PyFluent logger that outputs messages to stdout, but not to files."""
    logger = logging.getLogger("pyfluent")
    logger.setLevel("WARNING")
    formatter = logging.Formatter("%(name)s %(levelname)s: %(message)s")
    if not logger.handlers:
        ch = logging.StreamHandler()
        ch.setLevel("WARNING")
        ch.setFormatter(formatter)
        logger.addHandler(ch)


def is_active() -> bool:
    """Returns whether PyFluent logging to file is active."""
    return _logging_file_enabled


def get_default_config() -> dict:
    file_path = os.path.abspath(__file__)
    file_dir = os.path.dirname(file_path)
    yaml_path = os.path.join(file_dir, "logging_config.yaml")
    with open(yaml_path, "rt") as f:
        config = yaml.safe_load(f)
    return config


def enable(level: Union[str, int] = "DEBUG", custom_config: dict = None):
    """Enables PyFluent logging to file.

    Parameters
    ----------
    level : str or int, optional
        Specified logging level to set PyFluent loggers to. If omitted, level is set to DEBUG.
    custom_config : dict, optional
        Used to provide a customized logging config file.

    Notes
    -----
    See logging levels in https://docs.python.org/3/library/logging.html#logging-levels

    Examples
    --------
    >>> import ansys.fluent.core as pyfluent
    >>> pyfluent.logging.enable()
    """
    global _logging_file_enabled

    if _logging_file_enabled:
        print(
            "PyFluent logging to file is already active, overwriting previous configuration..."
        )

    _logging_file_enabled = True

    # Configure the logging system
    if custom_config is not None:
        config = custom_config
    else:
        config = get_default_config()

    logging.config.dictConfig(config)
    filename = config["handlers"]["pyfluent_file"]["filename"]

    print(f"PyFluent logging file {os.path.join(os.getcwd(),filename)}")

    set_global_level(level)


def get_logger(*args, **kwargs):
    """Retrieves logger. Convenience wrapper for Python's :func:`logging.getLogger` function."""
    return logging.getLogger(*args, **kwargs)


def set_global_level(level: Union[str, int]):
    """Changes the levels of all PyFluent loggers that write to log file.

    Parameters
    ----------
    level : str or int
        Specified logging level to set PyFluent loggers to.

    Notes
    -----
    See logging levels in https://docs.python.org/3/library/logging.html#logging-levels

    Examples
    --------
    >>> import ansys.fluent.core as pyfluent
    >>> pyfluent.logging.set_global_level(10)

    or

    >>> pyfluent.logging.set_global_level('DEBUG')
    """
    if not is_active():
        print("Logging is not active, enable it first.")
        return
    if isinstance(level, str):
        if level.isdigit():
            level = int(level)
        else:
            level = level.upper()
    print(f"Setting PyFluent global logging level to {level}.")
    pyfluent_loggers = list_loggers()
    for name in pyfluent_loggers:
        if name != "pyfluent":  # do not change the console root PyFluent logger
            logging.getLogger(name).setLevel(level)


def list_loggers():
    """List all PyFluent loggers.

    Returns
    -------
    list of str
        Each list element is a PyFluent logger name that can be individually controlled
        through :func:`ansys.fluent.core.logging.get_logger`.

    Notes
    -----
    PyFluent loggers use the standard Python logging library, for more details
    see https://docs.python.org/3/library/logging.html#logger-objects

    Examples
    --------
    >>> import ansys.fluent.core as pyfluent
    >>> pyfluent.logging.enable()
    >>> pyfluent.logging.list_loggers()
    ['pyfluent.general', 'pyfluent.launcher', 'pyfluent.networking', ...]
    >>> logger = pyfluent.logging.get_logger('pyfluent.networking')
    >>> logger
    <Logger pyfluent.networking (DEBUG)>
    >>> logger.setLevel('ERROR')
    >>> logger
    <Logger pyfluent.networking (ERROR)>
    """
    logger_dict = logging.root.manager.loggerDict
    pyfluent_loggers = []
    for name in logger_dict:
        if name.startswith("pyfluent"):
            pyfluent_loggers.append(name)
    return pyfluent_loggers


def configure_env_var() -> None:
    """Verifies whether PYFLUENT_LOGGING environment variable was defined in the system.
    Executed once automatically on PyFluent initialization.

    Notes
    -----
    The usual way to enable PyFluent logging to file is through :func:`enable()`.
    ``PYFLUENT_LOGGING`` set to ``0`` or ``OFF`` is the same as if no environment variable was set.
    If logging debug output to file is desired, without having to use :func:`enable()`,
    set ``PYFLUENT_LOGGING`` to ``DEBUG`` instead.
    See also the :ref:`logging user guide <ref_logging_env_var>`.
    """
    env_logging_level = os.getenv("PYFLUENT_LOGGING")
    if env_logging_level:
        if env_logging_level.isdigit():
            env_logging_level = int(env_logging_level)
        else:
            env_logging_level = env_logging_level.upper()
        if not is_active() and env_logging_level not in [0, "OFF"]:
            print(
                "PYFLUENT_LOGGING environment variable specified, enabling logging..."
            )
            enable(env_logging_level)
