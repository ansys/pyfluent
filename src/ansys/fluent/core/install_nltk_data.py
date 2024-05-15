"""Installs NLTK data."""

import platform
import subprocess
import sys


def install():
    """Install NLTK data."""
    if platform.system() == "Windows":
        subprocess.Popen(
            f"{sys.executable} -m nltk.downloader wordnet omw-1.4",
            stdout=subprocess.PIPE,
        )
    else:
        subprocess.Popen(
            f"{sys.executable} -m nltk.downloader wordnet omw-1.4",
            stdout=subprocess.PIPE,
            shell=True,
        )


if __name__ == "__main__":
    install()
