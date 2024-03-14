"""Get the git build info."""

from collections import OrderedDict
import subprocess

from ansys.fluent.core._version import __version__


def get_build_version():
    """Get build version."""
    build_details = OrderedDict()
    try:
        last_commit_time = (
            subprocess.check_output(["git", "log", "-n", "1", "--pretty=tformat:%ad"])
            .decode("ascii")
            .strip()
            .split()
        )
        time_zone = last_commit_time[5][:3] + ":" + last_commit_time[5][3:] + ":00"
        build_details["Build Time"] = (
            f"{last_commit_time[1]} {last_commit_time[2]} {last_commit_time[4]} {last_commit_time[3]} UTC{time_zone}"
        )
        build_details["Current Version"] = f"{__version__}"
        build_details["ShaID"] = (
            subprocess.check_output(["git", "rev-parse", "--short", "HEAD"])
            .decode("ascii")
            .strip()
        )
        build_details["Branch"] = (
            subprocess.check_output(["git", "branch", "--show-current"])
            .decode("ascii")
            .strip()
        )
    except Exception:
        pass
    return build_details


def get_build_version_string():
    """Get build version string."""
    return "  ".join([f"{k}: {v}" for k, v in get_build_version().items()])
