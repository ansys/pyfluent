from pathlib import Path
from tempfile import TemporaryDirectory
import uuid

from pytest import MonkeyPatch

import ansys.fluent.core as pyfluent
from ansys.fluent.core.codegen import StaticInfoType, datamodelgen
from ansys.fluent.core.utils import load_module


def create_datamodel_root_in_server(session, rules_str, app_name) -> None:
    rules_file_name = f"{uuid.uuid4()}.fdl"
    session.scheme_eval.scheme_eval(
        f'(with-output-to-file "{rules_file_name}" (lambda () (format "~a" "{rules_str}")))',
    )
    session.scheme_eval.scheme_eval(
        f'(state/register-new-state-engine "{app_name}" "{rules_file_name}")'
    )
    session.scheme_eval.scheme_eval(f'(remove-file "{rules_file_name}")')
    assert session.scheme_eval.scheme_eval(f'(state/find-root "{app_name}")') > 0


def create_root_using_datamodelgen(service, app_name):
    version = "252"
    static_info = service.get_static_info(app_name)
    with TemporaryDirectory() as temp_dir:
        with MonkeyPatch.context() as m:
            m.setattr(pyfluent, "CODEGEN_OUTDIR", Path(temp_dir))
            # TODO: Refactor datamdodelgen so we don't need to hardcode StaticInfoType
            datamodelgen.generate(
                version, static_infos={StaticInfoType.DATAMODEL_WORKFLOW: static_info}
            )
            gen_file = Path(temp_dir) / f"datamodel_{version}" / "workflow.py"
            module = load_module("datamodel", gen_file)
            return module.Root(service, app_name, [])
