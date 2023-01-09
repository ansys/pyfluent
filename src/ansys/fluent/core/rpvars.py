
import ansys.fluent.core.filereader.lispy as lispy


class RPVars:

    def __init__(self, eval_fn):
        self._eval_fn = eval_fn

    def __call__(self, var=None, val=None):
        return self._set_var(var, val) if val else (
            self._get_var(var) if var else self._get_vars()
        )

    def _get_var(self, var):
        cmd = f"(rpgetvar {self._var(var)})"
        return self._execute(cmd)

    def _get_vars(self):
        list_val = self._execute("(cx-send 'rp-variables)")
        return { val[0]: val[1] for val in list_val }

    def _set_var(self, var, val):
        prefix = "'" if isinstance(val, (list, tuple)) else ""
        cmd = f"(rpsetvar {self._var(var)} {prefix}{lispy.to_string(val)})"
        return self._execute(cmd)

    def _execute(self, cmd):
        scheme_val = self._eval_fn(cmd)
        return lispy.parse(scheme_val)

    @classmethod
    def _var(cls, var):
        if not var.startswith("'"):
            var = "'" + var
        return var
