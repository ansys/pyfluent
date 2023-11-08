from ansys.fluent.core import examples
from ansys.fluent.core.launcher.launcher import launch_fluent

import_file_name = examples.download_file(
    "mixing_elbow.msh.h5", "pyfluent/mixing_elbow"
)

solver = launch_fluent()
solver.read_case(import_file_name)

static_info = solver._settings_service.get_static_info()
solver.exit()

_items_with_file_name_arguments = set()


def _filter_items_with_file_name_arguments(info):
    for key, value in info.items():
        if isinstance(value, dict):
            if (
                "arguments" in value and "file-name" in value["arguments"]
            ):  # check for 'file-name' in arguments
                _items_with_file_name_arguments.add(key)
            _filter_items_with_file_name_arguments(value)


_filter_items_with_file_name_arguments(static_info)

print(_items_with_file_name_arguments)

# >>> _items_with_file_name_arguments
# {'compute-vf-only', 'specific-heat', 'write-case', 'computed-heat-rejection', 'fast-solution', 'mechanical-apdl', 'write-sample', 'heat-transfer-sensible', 'pressure-work', 'read-mesh', 'nastran', 'read-case', 'ensight', 'mass-weigh
# ted-avg', 'save-picture', 'fieldview-unstruct-surfaces', 'vertex-max', 'replace-mesh', 'mass-integral', 'volume', 'volume-integral', 'fieldview', 'vertex-avg', 'write-sc-file', 'taitherm', 'define-macro', 'integral', 'append-mesh',
# 'mass-flow', 'film-mass-flow', 'outlet-temperature', 'mass-average', 'vector-weighted-average', 'reduce-picked-sample', 'virtual-connection', 'read-vf-file', 'fieldview-unstruct', 'facet-min', 'read-field-functions', 'minimum', 'ens
# ight-gold-parallel-volume', 'read-pdf', 'compute-clusters-and-vf-accelerated', 'write-animation', 'mass-flow-rate', 'write-to-file', 'extended-summary', 'fast-velocity', 'maximum', 'replace', 'facet-avg', 'write-user-setting', 'appe
# nd-mesh-data', 'number-density', 'fieldview-unstruct-data', 'inlet-temperature', 'read-case-setting', 'read-data', 'heat-transfer', 'ideas', 'write-views', 'ensight-gold-parallel-surfaces', 'read', 'electric-current', 'export-simula
# tion-report-as-pdf', 'standard-deviation', 'replace-zone', 'icemcfd-for-icepak', 'abaqus', 'read-injections', 'volume-flow-rate', 'vbm', 'summary', 'read-settings', 'mass', 'write-all-to-file', 'read-case-data', 'read-macros', 'film
# -heat-transfer', 'vertex-min', 'uniformity-index-area-weighted', 'ensight-gold', 'vector-based-flux', 'start-journal', 'flow-rate', 'facet-max', 'write-case-data', 'area', 'write-simulation-report-names-to-file', 'export-simulation-
# report-as-pptx', 'vector-flux', 'custom-heat-flux', 'read-input-file', 'sum', 'tecplot', 'write', 'read-profile', 'avs', 'viscous-work', 'radiation-heat-transfer', 'forces', 'read-animation', 'dx', 'compute-write-vf', 'gambit', 'rea
# d-isat-table', 'fast-mesh', 'uniformity-index-mass-weighted', 'fieldview-unstruct-mesh', 'fieldview-data', 'cgns', 'compute-vf-accelerated', 'volume-average', 'write-data', 'patran-neutral', 'mechanical-apdl-input', 'write-scp-file'
# , 'twopisum', 'ascii', 'write-simulation-report-template-file', 'start-transcript', 'patran-nodal', 'area-weighted-avg', 'read-simulation-report-template-file', 'plot-sample', 'import-fmu'}
