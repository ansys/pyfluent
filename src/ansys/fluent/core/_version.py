"""Version of ansys-fluent-core module.

On the ``main`` branch, use 'dev0' to denote a development version.
For example:
version_info = 0, 1, 'dev0'
"""

# major, minor, patch
version_info = 0, 26, 1

# Nice string for the version
__version__ = ".".join(map(str, version_info))

# Current Fluent version
fluent_release_version = "25.1.0"
