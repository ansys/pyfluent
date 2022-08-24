import os

import ansys.fluent.core as pyfluent


def get_version(session=None):
    if session is None:
        # for CI runs, get the version statically from env var set within CI
        image_tag = os.getenv("FLUENT_IMAGE_TAG")
        if image_tag is not None:
            return image_tag.lstrip("v")
        session = pyfluent.launch_fluent(mode="solver")

    try:
        return (
            session.get_fluent_version()
        )  # doesn't work in meshing tuigen with docker
    except AttributeError:
        return ".".join(
            map(str, session._fluent_connection.scheme_eval.scheme_eval("(cx-version)"))
        )


def get_version_for_filepath(version: str = None, session=None):
    if version is None:
        version = get_version(session)

    return "".join(version.split(".")[0:2])


default_version = "22.2.0"
default_version_for_filepath = get_version_for_filepath(default_version)
