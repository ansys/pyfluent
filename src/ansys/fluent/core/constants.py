"""PyFluent constants."""

import asyncio
import os
from typing import Dict, List, NewType, Sequence, Tuple, TypeVar, Union

from ansys.fluent.core.utils import get_user_data_dir

loop = asyncio.get_event_loop()

log_bytes_limit: int = int(os.getenv("PYFLUENT_GRPC_LOG_BYTES_LIMIT", 1000))
truncate_len: int = log_bytes_limit // 5

ContainerT = TypeVar("ContainerT")

ChildTypeT = TypeVar("ChildTypeT")

DEPRECATION_MSG = "'field_data_old' is deprecated. Use 'field_data' instead."

indent_factor = 2

# Host path which is mounted to the file-transfer-service container
MOUNT_SOURCE = str(get_user_data_dir())

name_to_identifier_map = {
    "Watertight Geometry": "EnableCleanCAD",
    "Fault-tolerant Meshing": "EnableComplexMeshing",
    "2D Meshing": "EnablePrime2dMeshing",
    "Topology Based Meshing": "EnablePrimeMeshing",
}

Path = list[str]
ValueT = None | bool | int | float | str | Sequence["ValueT"] | dict[str, "ValueT"]

QuantityT = TypeVar("QuantityT")

# Root domain id in Fluent.
ROOT_DOMAIN_ID = 1

StateT = TypeVar("StateT")

StateType = (
    bool
    | int
    | float
    | str
    | List[bool]
    | List[int]
    | List[float]
    | List[str]
    | List["StateType"]
    | Dict[str, "StateType"]
)

TEvent = TypeVar("TEvent")

trace: bool = False

WATCHDOG_INIT_FILE = "watchdog_{}_init"

# Type hints
RealType = NewType("real", Union[float, str])  # constant or expression
RealListType = List[RealType]
RealVectorType = Tuple[RealType, RealType, RealType]
IntListType = List[int]
StringListType = List[str]
BoolListType = List[bool]
PrimitiveStateType = Union[
    str,
    RealType,
    int,
    bool,
    RealListType,
    IntListType,
    StringListType,
    BoolListType,
]
DictStateType = Dict[str, "StateType"]
ListStateType = List["StateType"]
StateType = Union[PrimitiveStateType, DictStateType, ListStateType]

# this can be switched to False in scenarios where the field_data request inputs are
# fed by results of field_info queries, which might be true in GUI code.
validate_inputs = True

XML_HELP_PATCH = {
    "flu_meshing_file_start_transcript": "Starts recording input and output in a file. A transcript file contains a complete record of all standard input to and output from Fluent (usually all keyboard and user interface input and all screen output).Start the transcription process with the file/start-transcript command, and end it with the file/stop-transcript command (or by exiting the program)."
}


_bases_by_class = {}

_CODEGEN_MSG_DATAMODEL = (
    "Currently calling the datamodel API in a generic manner. "
    "Please run `python codegen/allapigen.py` from the top-level pyfluent "
    "directory to generate the local datamodel API classes."
)

_CODEGEN_MSG_TUI = (
    "Currently calling the TUI commands in a generic manner. "
    "Please run `python codegen/allapigen.py` from the top-level pyfluent "
    "directory to generate the local TUI commands classes."
)

_fl_unit_table = {
    "acceleration": "m s^-2",
    "angle": "radian",
    "angular-velocity": "radian s^-1",
    "area": "m^2",
    "area-inverse": "m^-2",
    "collision-rate": "m^-3 s^-1",
    "contact-resistance": "m^2 K W^-1",
    "contact-resistance-vol": "ohm m^3",
    "crank-angle": "radian",
    "current": "A",
    "current-density": "A m^-2",
    "current-vol-density": "A m^-3",
    "density": "kg m^-3",
    "density*specific-energy": "J m^-3",
    "density*specific-heat": "J m^-3 K^-1",
    "density*velocity": "kg m^-2 s^-1",
    "density-gradient": "kg m^-4",
    "density-inverse": "m^3 kg^-1",
    "depth": "m",
    "elec-charge-density": "A s m^-3",
    "elec-conductivity": "S m^-1",
    "elec-contact-resistance": "ohm m^2",
    "elec-field": "V m^-1",
    "elec-permittivity": "farad m^-1",
    "elec-resistance": "ohm",
    "elec-resistivity": "ohm m",
    "energy": "J",
    "force": "N",
    "force*time-per-volume": "N s m^-3",
    "force-per-area": "N m^-2",
    "force-per-volume": "N m^-3",
    "frequency": "Hz",
    "gas-constant": "J kg^-1 K^-1",
    "heat-flux": "W m^-2",
    "heat-flux-resolved": "m K s^-1",
    "heat-generation-rate": "W m^-3",
    "heat-transfer-coefficient": "W m^-2 K^-1",
    "ignition-energy": "J mol^-1",
    "kinematic-viscosity": "m^2 s^-1",
    "length": "m",
    "length-inverse": "m^-1",
    "length-time-inverse": "m^-1 s^-1",
    "mag-permeability": "H m^-1",
    "mass": "kg",
    "mass-diffusivity": "m^2 s^-1",
    "mass-flow": "kg s^-1",
    "mass-flow-per-depth": "kg m^-1 s^-1",
    "mass-flow-per-time": "kg s^-2",
    "mass-flux": "kg m^-2 s^-1",
    "mass-transfer-rate": "kg m^-3 s^-1",
    "moment": "N m",
    "moment-of-inertia": "kg m^2",
    "nucleation-rate": "m^-3 s^-1",
    "number-density": "m^-3",
    "percentage": "",
    "power": "W",
    "power-per-time": "W s^-1",
    "pressure": "Pa",
    "pressure-2nd-time-derivative": "Pa s^-2",
    "pressure-gradient": "Pa m^-1",
    "pressure-time-deriv-sqr": "Pa^2 s^-2",
    "pressure-time-derivative": "Pa s^-1",
    "resistance": "m^-1",
    "soot-formation-constant-unit": "kg N^-1 m^-1 s^-1",
    "soot-linear-termination": "m^3 s^-1",
    "source-elliptic-relaxation-function": "kg m^-3 s^-2",
    "source-energy": "W m^-3",
    "source-kinetic-energy": "kg m^-1 s^-3",
    "source-mass": "kg m^-3 s^-1",
    "source-momentum": "N m^-3",
    "source-specific-dissipation-rate": "kg m^-3 s^-2",
    "source-temperature-variance": "K^2 m^-3 s^-1",
    "source-turbulent-dissipation-rate": "kg m^-1 s^-4",
    "source-turbulent-viscosity": "kg m^-1 s^-2",
    "specific-area": "m^2 kg^-1",
    "specific-energy": "J kg^-1",
    "specific-heat": "J kg^-1 K^-1",
    "spring-constant": "N m^-1",
    "spring-constant-angular": "N m radian^-1",
    "stefan-boltzmann-constant": "W m^-2 K^-4",
    "surface-density": "kg m^-2",
    "surface-tension": "N m^-1",
    "surface-tension-gradient": "N m^-1 K^-1",
    "temperature": "K",
    "temperature-difference": "K",
    "temperature-gradient": "K m^-1",
    "temperature-inverse": "K^-1",
    "temperature-variance": "K^2",
    "thermal-conductivity": "W m^-1 K^-1",
    "thermal-resistance": "m^2 K W^-1",
    "thermal-resistivity": "m K W^-1",
    "thermophoretic-diffusivity": "kg m^2 s^-2",
    "time": "s",
    "time-inverse": "s^-1",
    "time-inverse-cubed": "s^-3",
    "time-inverse-squared": "s^-2",
    "turb-kinetic-energy-production": "kg m^-1 s^-3",
    "turbulent-energy-diss-rate": "m^2 s^-3",
    "turbulent-energy-diss-rate-gradient": "m s^-3",
    "turbulent-kinetic-energy": "m^2 s^-2",
    "turbulent-kinetic-energy-gradient": "m s^-2",
    "velocity": "m s^-1",
    "viscosity": "kg m^-1 s^-1",
    "voltage": "V",
    "volume": "m^3",
    "volume-flow-rate": "m^3 s^-1",
    "volume-flow-rate-per-depth": "m^3 s^-1 m^-1",
    "volume-inverse": "m^-3",
    "youngs-modulus": "N m^-2",
}

_indent: int = 0

_INDENT_STEP = 4

_logging_file_enabled = False

# Store the top level class names and their data hash.
# This is used to avoid name collisions and data duplication.
_NAME_BY_HASH = {}

_PY_TYPE_BY_DM_TYPE = {
    **dict.fromkeys(["Logical", "Bool"], "bool"),
    **dict.fromkeys(["Logical List", "ListBool"], "list[bool]"),
    "String": "str",
    **dict.fromkeys(["String List", "ListString"], "list[str]"),
    **dict.fromkeys(["Integer", "Int"], "int"),
    **dict.fromkeys(["Integer List", "ListInt"], "list[int]"),
    "Real": "float",
    **dict.fromkeys(
        [
            "Real List",
            "ListReal",
            "Real Triplet",
            "RealTriplet",
            "Real Triplet List",
            "ListRealTriplet",
        ],
        "list[float]",
    ),
    **dict.fromkeys(["Dict", "ModelObject"], "dict[str, Any]"),
    "None": "None",
}

# Keeps tracks of which classes have been written to the file.
# See the implementation note in _write_data() for more details.
_CLASS_WRITTEN = set()

_ncoresOpt = "-t%n%"
_machinesOpt = " -cnf=%machineList%"
_procSep = ":"
_machineSep = ","

_XML_HELPSTRINGS = {}
