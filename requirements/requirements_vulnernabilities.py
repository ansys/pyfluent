"""This module installs the required packages for the vulnerabilities check."""

import subprocess
import sys

try:
    import bandit.cli.main as bandit  # noqa: F401
    import click  # noqa: F401
    import github  # noqa: F401
    import safety.cli as safety  # noqa: F401
except ModuleNotFoundError:
    subprocess.run(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            "click>=7.0,<9",
            "PyGithub>=1.59,<2",
            "bandit>=1.7,<2",
            "safety>=2.3,<4",
        ]
    )
