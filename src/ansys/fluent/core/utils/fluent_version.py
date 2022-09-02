import os

import ansys.fluent.core as pyfluent
from ansys.fluent.core.services.scheme_eval import SchemeEval, SchemeEvalService


def get_version(session=None):
    if session is None:
        # for CI runs, get the version statically from env var set within CI
        image_tag = os.getenv("FLUENT_IMAGE_TAG")
        if image_tag is not None:
            return image_tag.lstrip("v")
        session = pyfluent.launch_fluent(mode="solver")

    return session.get_fluent_version()


def get_version_for_filepath(version: str = None, session=None):
    if version is None:
        version = get_version(session)

    return "".join(version.split(".")[0:2])


def get_version_for_filepath_lite(channel, metadata):
    scheme_eval_service = SchemeEvalService(channel, metadata)
    scheme_eval = SchemeEval(scheme_eval_service)
    return "".join(map(str, scheme_eval.scheme_eval("(cx-version)")[0:2]))
