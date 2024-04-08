"""Provides a module to check if the application is running in notebook."""


def in_notebook():
    """Checks if the application is running in notebook."""
    try:
        from IPython import get_ipython

        if "IPKernelApp" not in get_ipython().config:
            return False
    except (ImportError, AttributeError):
        return False
    return True
