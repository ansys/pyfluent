"""Global configuration state for post."""
import threading

_global_config = {"blocking": False, "set_view_on_display": None}
_threadlocal = threading.local()


def _get_threadlocal_config():
    if not hasattr(_threadlocal, "global_config"):
        _threadlocal.global_config = _global_config.copy()
    return _threadlocal.global_config


def get_config() -> dict:
    """Retrieve post configuration.

    Returns
    -------
    config : dict
        Keys are parameter names that can be passed to :func:`set_config`.
    """
    return _get_threadlocal_config().copy()


def set_config(blocking: bool = False, set_view_on_display: str = None):
    """Set post configuration.

    Parameters
    ----------
    blocking : bool, default=False
        If True, then graphics/plot display will block the current thread.
    set_view_on_display : str, default=None
        If specified, then graphics will always be displayed in the specified view.
        Valid values are xy, xz, yx, yz, zx, zy and isometric.
    """
    local_config = _get_threadlocal_config()
    local_config["blocking"] = blocking
    local_config["set_view_on_display"] = set_view_on_display
