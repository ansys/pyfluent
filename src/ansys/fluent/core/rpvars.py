# Copyright (C) 2021 - 2026 ANSYS, Inc. and/or its affiliates.
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

"""Client-side service allowing access and modification of rpvars.

The primary interaction with Fluent should not be through low-level
variables like rpvars but instead through the high-level object-based
interfaces: solver settings objects and task-based meshing workflow.
"""
from enum import Enum
from typing import Any, List

import ansys.fluent.core.filereader.lispy as lispy
from ansys.fluent.core.solver.error_message import allowed_name_error_message


class RPVarType(Enum):
    """Enumeration of rpvar types mapping Python types to Fluent type strings."""

    INTEGER = "integer"
    REAL = "real"
    BOOLEAN = "boolean"
    STRING = "string"
    CUSTOM = "none"

    @classmethod
    def from_python_type(cls, python_type: type) -> "RPVarType":
        """Convert Python type to RPVarType.

        Parameters
        ----------
        python_type : type
            Python type to convert.

        Returns
        -------
        RPVarType
            Corresponding RPVarType enum value.

        Raises
        ------
        ValueError
            For unsupported python types.
        """
        type_map = {
            int: cls.INTEGER,
            float: cls.REAL,
            bool: cls.BOOLEAN,
            str: cls.STRING,
        }
        if python_type not in type_map:
            raise ValueError(f"Unsupported type: {python_type}")
        return type_map[python_type]


class RPVars:
    """Access to rpvars in a specific session."""

    def __init__(self, eval_fn):
        """Initialize RPVars."""
        self._eval_fn = eval_fn

    def __call__(self, var: str | None = None, val: Any | None = None) -> Any:
        """Set or get a specific rpvar, or get the full rpvar state.

        Parameters
        ----------
        var : str
            Name of the rpvar. Set the specified rpvar if val is provided,
            or else return its value.
        val : Any
            Value of the rpvar. Set the specified var to this value if val
            is specified.

        Returns
        -------
        Any
            A dict containing the full rpvar state if all arguments are
            unspecified, the value of the rpvar if only var is specified,
            or a string with the var name if both arguments are specified.

        Examples
        --------
        >>> import ansys.fluent.core as pyfluent
        >>> solver = pyfluent.launch_fluent(mode="solver")
        >>> iter_count = 100
        >>> solver.rp_vars("number-of-iterations", iter_count)
        'number-of-iterations'
        >>> solver.rp_vars("number-of-iterations")
        100

        >>> # Get dictionary of all available rpvars:

        >>> solver.rp_vars()
        {'sg-swirl?': False, 'rp-seg?': True, 'rf-energy?': False, 'rp-inviscid?': False, ...
        'number-of-iterations': 100, ...}
        """
        return (
            self._set_var(var, val)
            if val is not None
            else (self._get_var(var) if var is not None else self._get_vars())
        )

    def allowed_values(self) -> List[str]:
        """Returns list with the allowed rpvars names.

        Returns
        -------
        List[str]
            List with all allowed rpvars names.
        """
        return lispy.parse(self._eval_fn("(cx-send '(map car rp-variables))"))

    def _get_var(self, var: str):
        allowed_rp_vars = self.allowed_values()
        if var not in allowed_rp_vars:
            raise RuntimeError(
                allowed_name_error_message(
                    context="rp-vars",
                    trial_name=var,
                    allowed_values=allowed_rp_vars,
                )
            )

        cmd = f"(rpgetvar {RPVars._var(var)})"
        return self._execute(cmd)

    def _get_vars(self):
        list_val = self._execute("(cx-send 'rp-variables)")
        return {val[0]: val[1] for val in list_val}

    def _set_var(self, var: str, val):
        prefix = "'" if isinstance(val, (list, tuple)) else ""
        if type(val) is str:
            cmd = f'(rpsetvar {RPVars._var(var)} {prefix}"{lispy.to_string(val)}")'
        else:
            cmd = f"(rpsetvar {RPVars._var(var)} {prefix}{lispy.to_string(val)})"
        return self._execute(cmd)

    def create(self, name: str, value: Any, var_type: RPVarType | type | None):
        """Create a new rpvar.

        Parameters
        ----------
        name : str
            Name of the rpvar to create.
        value : Any
            Initial value for the rpvar.
        var_type : RPVarType | type | None
            Type of the rpvar, either as RPVarType enum or Python type.
            Allowed Python types: int, float, bool, str or None.

        Raises
        ------
        NameError
            If the rpvar name already exists.
        TypeError
            If the value type doesn't match the specified var_type.
        """
        if var_type is None:
            var_type = RPVarType.CUSTOM
            python_type = None
        elif isinstance(var_type, type):
            python_type = var_type
            var_type = RPVarType.from_python_type(var_type)
        elif isinstance(var_type, RPVarType):
            type_map = {
                RPVarType.INTEGER: int,
                RPVarType.REAL: float,
                RPVarType.BOOLEAN: bool,
                RPVarType.STRING: str,
            }
            python_type = type_map.get(var_type)
        else:
            raise TypeError(
                "Invalid var_type: expected RPVarType enum, Python type, or None."
            )

        # Type check the value
        if python_type and var_type != RPVarType.CUSTOM:
            type_mismatch = False
            if python_type is int:
                # Avoid accepting booleans where a strict integer is expected
                type_mismatch = type(value) is not int
            elif python_type is bool:
                # Enforce strict boolean type as well
                type_mismatch = type(value) is not bool
            else:
                type_mismatch = not isinstance(value, python_type)
            if type_mismatch:
                raise TypeError(
                    f"Value type mismatch: expected {python_type}, got {type(value).__name__}"
                )
        prefix = "'" if isinstance(value, (list, tuple)) else ""
        if var_type == RPVarType.STRING:
            cmd = f'(make-new-rpvar {RPVars._var(name)} "{prefix}{lispy.to_string(value)}" \'{lispy.to_string(var_type.value)})'
        else:
            cmd = f"(make-new-rpvar {RPVars._var(name)} {prefix}{lispy.to_string(value)} '{lispy.to_string(var_type.value)})"
        returned_val = self._execute(cmd)
        if returned_val is False:
            if name in self.allowed_values():
                raise NameError(f"'{name}' already exists as an rpvar.")
        else:
            return returned_val

    def _execute(self, cmd: str):
        scheme_val = self._eval_fn(cmd)
        return lispy.parse(scheme_val)

    @staticmethod
    def _var(var: str):
        if not var.startswith("'"):
            var = "'" + var
        return var
