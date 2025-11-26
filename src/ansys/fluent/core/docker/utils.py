# Copyright (C) 2021 - 2025 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
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

"""
Utility functions for working with Fluent Docker images.
"""


import os


def _is_grpc_patched(image_tag: str):
    """
    Check if the image tag corresponds to a version that patches gRPC.
    """
    if image_tag.startswith("sha256:"):
        return True

    min_patched_versions = {
        "v25.2": 3,
        "v25.1": 4,
        "v24.2": 5,
    }
    for version, min_patch in min_patched_versions.items():
        if image_tag.startswith(version) and image_tag.count(".") == 2:
            patch_version = int(image_tag.split(".")[-1])
            return patch_version >= min_patch
    return False


def get_grpc_launcher_args_for_gh_runs():
    """
    Get the gRPC launcher arguments for GitHub Actions runs based on the Fluent image tag.
    """
    kwds = {}
    fluent_image_tag = os.getenv("FLUENT_IMAGE_TAG")
    if fluent_image_tag:
        if _is_grpc_patched(fluent_image_tag) and not fluent_image_tag.startswith(
            "v24.2"
        ):
            kwds["certificates_folder"] = os.path.join(os.getcwd(), "certs")
        else:
            kwds["insecure_mode"] = True
    return kwds


def get_ghcr_fluent_image_name(image_tag: str):
    """
    Get the Fluent image name from GitHub registry based on the image tag.
    """
    if (
        image_tag.startswith("sha256:")
        or image_tag >= "v26.1"
        or _is_grpc_patched(image_tag)
    ):
        return "ghcr.io/ansys/fluent"
    else:
        return "ghcr.io/ansys/pyfluent"
