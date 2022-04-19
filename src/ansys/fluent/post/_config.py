"""Global configuration state for post."""
import threading

_global_config = {
    "blocking": False,
}
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


def set_config(blocking: bool = False):
    """Set post configuration.

    Parameters
    ----------
    blocking : bool, default=False
        If True, then graphics/plot display will block the current thread.
    """
    local_config = _get_threadlocal_config()
    local_config["blocking"] = blocking
