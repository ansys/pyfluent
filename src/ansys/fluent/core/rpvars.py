"""Client-side service allowing access and modification of rpvars.

The primary interaction with Fluent should not be through low-level
variables like rpvars but instead through the high-level object-based
interfaces: solver settings objects and task-based meshing workflow.
"""
import difflib
from functools import partial
from typing import Any, List

import ansys.fluent.core.filereader.lispy as lispy

_allowed_rpvars_values = []


class RPVars:
    """Access to rpvars in a specific session.

    Methods
    -------
    __call__(
        var, val
        )
        Set or get a specific rpvar or get the full rpvar state.
    """

    def __init__(self, eval_fn):
        self._eval_fn = eval_fn

    def __call__(self, var: str = None, val: Any=None) -> Any:
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

        return self._set_var(var, val) if val else (
            self._get_var(var) if var else self._get_vars()
        )

    def allowed_values(self) -> List[str]:
        if not _allowed_rpvars_values:
            _allowed_rpvars_values.append(lispy.parse(self._eval_fn("(cx-send '(map car rp-variables))")))
        return _allowed_rpvars_values[0]

    @staticmethod
    def closest_allowed_names(trial_name: str, allowed_names: str) -> List[str]:
        f = partial(difflib.get_close_matches, trial_name, allowed_names)
        return f(cutoff=0.6, n=5) or f(cutoff=0.3, n=1)

    def allowed_name_error_message(
            self,
            context: str, trial_name: str, allowed_values: List[str]
    ) -> str:
        message = f"{trial_name} is not an allowed {context} name.\n"
        matches = self.closest_allowed_names(trial_name, allowed_values)
        if matches:
            message += f"The most similar names are: {', '.join(matches)}."
        return message

    def _get_var(self, var: str):
        if not _allowed_rpvars_values:
            _allowed_rpvars_values.append(self.allowed_values())
        if var not in _allowed_rpvars_values[0]:
            raise RuntimeError(self.allowed_name_error_message("", var, _allowed_rpvars_values[0]))

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
