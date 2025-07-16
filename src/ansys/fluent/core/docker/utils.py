"""
Utility functions for working with Fluent Docker images.
"""


def get_ghcr_fluent_image_name(image_tag: str):
    """
    Get the Fluent image name from GitHub registry based on the image tag.
    """
    if image_tag >= "v26.1":
        return "ghcr.io/ansys/fluent"
    else:
        return "ghcr.io/ansys/pyfluent"
