# Copyright (C) 2021 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT
#
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Configure and control PyFluent logging.

This module builds on Python's standard :mod:`logging` package and provides
PyFluent-specific defaults and helpers. PyFluent messages use the ``pyfluent``
logger hierarchy and are written to the console at warning level by default.
File logging can be enabled with :func:`enable`, which uses a rotating file
handler and the configuration in ``logging_config.yaml``. The
``PYFLUENT_LOGGING`` environment variable can enable file logging
automatically during PyFluent initialization.

The public helpers support enabling file logging, changing console and file log
levels, checking whether file logging is active, obtaining a logger, loading
the default configuration, and providing a custom logging configuration.
Startup and logger-discovery helpers are kept internal to the module.
"""

import logging.config
import os

from ansys.fluent.core.module_config import config

__all__ = (
    "enable",
    "get_default_config",
    "get_logger",
    "is_active",
    "set_console_logging_level",
    "set_global_level",
)

_logging_file_enabled = False


def root_config():
    """Sets up the root PyFluent logger that outputs messages to stdout, but not to
    files."""
    logger = logging.getLogger("pyfluent")
    logger.setLevel("WARNING")
    formatter = logging.Formatter("%(name)s %(levelname)s: %(message)s")
    if not logger.handlers:
        ch = logging.StreamHandler()
        ch.setLevel("WARNING")
        ch.setFormatter(formatter)
        logger.addHandler(ch)


def set_console_logging_level(level: str | int):
    """Set the minimum level of PyFluent messages written to the console.

    Parameters
    ----------
    level : str or int
        Logging level, such as ``"INFO"``, ``"DEBUG"``, or ``logging.INFO``.
        Messages below this level are filtered from the console handler.

    Notes
    -----
    This changes console output only. Use :func:`set_global_level` to change
    the levels of loggers writing to the PyFluent log file.
    See logging levels in https://docs.python.org/3/library/logging.html#logging-levels

    Examples
    --------
    >>> import ansys.fluent.core as pyfluent
    >>> pyfluent.set_console_logging_level("INFO")
    """
    logger = logging.getLogger("pyfluent")
    logger.setLevel(level)
    for ch in logger.handlers:
        ch.setLevel(level)


def is_active() -> bool:
    """Return whether PyFluent file logging is currently enabled.

    Returns
    -------
    bool
        ``True`` after :func:`enable` has configured file logging; otherwise
        ``False``.
    """
    return _logging_file_enabled


def get_default_config() -> dict:
    """Load PyFluent's default logging configuration.

    Returns
    -------
    dict
        A dictionary parsed from PyFluent's ``logging_config.yaml`` file. The
        dictionary can be modified and passed to :func:`enable` through its
        ``custom_config`` parameter.

    Examples
    --------
    >>> import ansys.fluent.core as pyfluent
    >>> pyfluent.logger.get_default_config()
    {'disable_existing_loggers': False,
     'formatters': {'logfile_fmt': {'format': '%(asctime)s %(name)-21s '
                                              '%(levelname)-8s %(message)s'}},
     'handlers': {'pyfluent_file': {'backupCount': 9,
                                    'class': 'logging.handlers.RotatingFileHandler',
                                    'filename': 'pyfluent.log',
                                    'formatter': 'logfile_fmt',
                                    'level': 'NOTSET',
                                    'maxBytes': 10485760}},
     'loggers': {'pyfluent.datamodel': {'handlers': ['pyfluent_file'],
                                        'level': 'DEBUG'},
                 'pyfluent.expressions': {'handlers': ['pyfluent_file'],
                                           'level': 'DEBUG'},
                 'pyfluent.field_data': {'handlers': ['pyfluent_file'],
                                         'level': 'DEBUG'},
                 'pyfluent.general': {'handlers': ['pyfluent_file'],
                                      'level': 'DEBUG'},
                 'pyfluent.launcher': {'handlers': ['pyfluent_file'],
                                       'level': 'DEBUG'},
                 'pyfluent.networking': {'handlers': ['pyfluent_file'],
                                         'level': 'DEBUG'},
                 'pyfluent.settings_api': {'handlers': ['pyfluent_file'],
                                           'level': 'DEBUG'},
                 'pyfluent.tui': {'handlers': ['pyfluent_file'], 'level': 'DEBUG'}},
     'version': 1}
    """
    import yaml

    file_name = os.path.abspath(__file__)
    file_dir = os.path.dirname(file_name)
    yaml_path = os.path.join(file_dir, "logging_config.yaml")
    with open(yaml_path) as f:
        config = yaml.safe_load(f)
    return config


def enable(level: str | int = "DEBUG", custom_config: dict | None = None):
    """Enable PyFluent logging to a rotating log file.

    By default, PyFluent uses the packaged ``logging_config.yaml`` file and
    writes to ``pyfluent.log`` in the current working directory. Calling this
    function again reconfigures logging with the supplied configuration.

    Parameters
    ----------
    level : str or int, optional
        Minimum level for PyFluent loggers writing to the file. If omitted,
        ``"DEBUG"`` is used.
    custom_config : dict, optional
        A ``logging.config.dictConfig``-compatible configuration. Use
        :func:`get_default_config` as a starting point when customizing the
        default configuration.

    Notes
    -----
    File logging can also be enabled automatically by setting the
    ``PYFLUENT_LOGGING`` environment variable before importing PyFluent.

    See Also
    --------
    get_default_config
        Load the packaged logging configuration for customization.

    Examples
    --------
    Using the default logging setup:

    >>> import ansys.fluent.core as pyfluent
    >>> pyfluent.logger.enable()

    Customizing logging configuration (see also :func:`get_default_config`):

    >>> import ansys.fluent.core as pyfluent
    >>> config_dict = pyfluent.logger.get_default_config()
    >>> config_dict['handlers']['pyfluent_file']['filename'] = 'test.log'
    >>> pyfluent.logger.enable(custom_config=config_dict)
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
    file_name = config["handlers"]["pyfluent_file"]["filename"]

    print(f"PyFluent logging file {os.path.join(os.getcwd(), file_name)}")

    set_global_level(level)


def get_logger(*args, **kwargs):
    """Return a standard-library logger for a PyFluent component.

    Parameters
    ----------
    *args, **kwargs
        Arguments forwarded to :func:`logging.getLogger`. Passing a name such
        as ``"pyfluent.launcher"`` is recommended for component-specific
        logging.

    Returns
    -------
    logging.Logger
        The requested logger instance.

    Examples
    --------
    >>> import ansys.fluent.core as pyfluent
    >>> logger = pyfluent.get_logger("pyfluent.my_component")
    >>> logger.info("Component initialized")
    """
    return logging.getLogger(*args, **kwargs)


def set_global_level(level: str | int):
    """Set the level of all registered PyFluent file loggers.

    Parameters
    ----------
    level : str or int
        Logging level, such as ``"DEBUG"``, ``"INFO"``, or ``logging.WARNING``.

    Notes
    -----
    File logging must be enabled with :func:`enable` first. This function does
    not change the console logger level; use :func:`set_console_logging_level`
    for console output.

    Examples
    --------
    >>> import ansys.fluent.core as pyfluent
    >>> pyfluent.enable()
    >>> pyfluent.set_global_level("INFO")

    Examples
    --------
    >>> import ansys.fluent.core as pyfluent
    >>> pyfluent.logger.set_global_level(10)

    or

    >>> pyfluent.logger.set_global_level('DEBUG')
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
    >>> pyfluent.logger.enable()
    >>> pyfluent.logger.list_loggers()
    ['pyfluent.general', 'pyfluent.launcher', 'pyfluent.networking', ...]
    >>> logger = pyfluent.logger.get_logger('pyfluent.networking')
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
    """Verifies whether ``PYFLUENT_LOGGING`` environment variable was defined in the
    system. Executed once automatically on PyFluent initialization.

    Notes
    -----
    The usual way to enable PyFluent logging to file is through :func:`enable()`.
    ``PYFLUENT_LOGGING`` set to ``0`` or ``OFF`` is the same as if no environment variable was set.
    If logging debug output to file by default is desired, without having to use :func:`enable()` every time,
    set environment variable ``PYFLUENT_LOGGING`` to ``DEBUG``.
    """
    env_logging_level = config.logging_level_default
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


root_config()
configure_env_var()
