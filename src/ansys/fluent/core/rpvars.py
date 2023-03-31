"""Client-side service allowing access and modification of rpvars.

The primary interaction with Fluent should not be through low-level
variables like rpvars but instead through the high-level object-based
interfaces: solver settings objects and task-based meshing workflow.
"""
from typing import Any, List

import ansys.fluent.core.filereader.lispy as lispy
from ansys.fluent.core.solver.error_message import allowed_name_error_message


class RPVars:
    """Access to rpvars in a specific session.

    Methods
    -------
    __call__(var, val)
        Set or get a specific rpvar or get the full rpvar state.
    """

    _allowed_values = None

    def __init__(self, eval_fn):
        self._eval_fn = eval_fn

    def __call__(self, var: str = None, val: Any = None) -> Any:
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
            unspecified, or the value of the rpvar if only var is specified,
            or None if both arguments are specified.
        """
        return (
            self._set_var(var, val)
            if val
            else (self._get_var(var) if var else self._get_vars())
        )

    def allowed_values(self) -> List[str]:
        if not RPVars._allowed_values:
            RPVars._allowed_values = lispy.parse(
                self._eval_fn("(cx-send '(map car rp-variables))")
            )
        return RPVars._allowed_values

    def _get_var(self, var: str):
        if var not in self.allowed_values():
            raise RuntimeError(
                allowed_name_error_message("rp-vars", var, RPVars._allowed_values)
            )

        cmd = f"(rpgetvar {RPVars._var(var)})"
        return self._execute(cmd)

    def _get_vars(self):
        list_val = self._execute("(cx-send 'rp-variables)")
        return {val[0]: val[1] for val in list_val}

    def _set_var(self, var: str, val):
        prefix = "'" if isinstance(val, (list, tuple)) else ""
        cmd = f"(rpsetvar {RPVars._var(var)} {prefix}{lispy.to_string(val)})"
        return self._execute(cmd)

    def _execute(self, cmd: str):
        scheme_val = self._eval_fn(cmd)
        return lispy.parse(scheme_val)

    @staticmethod
    def _var(var: str):
        if not var.startswith("'"):
            var = "'" + var
        return var
