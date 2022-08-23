import json


class MeshingMeshing:
    def __init__(self, meshing, tui, fluent_connection):
        self._meshing = meshing
        self._tui = tui
        self._fluent_connection = fluent_connection
        self.switch_to_solver = lambda: self._switch_to_solver()

    def execute_tui(self, command: str) -> None:
        """Executes a tui command."""
        self._fluent_connection.scheme_eval.scheme_eval(
            f'(tui-menu-execute {json.dumps(command)} "")'
        )

    def _switch_to_solver(self):
        from ansys.fluent.core.session_solver import Solver

        self._tui.switch_to_solution_mode("yes")
        solver_session = Solver(fluent_connection=self._fluent_connection)
        return solver_session

    def __getattr__(self, attr):
        return getattr(self._meshing, attr)

    def __dir__(self):
        return sorted(
            set(list(self.__dict__.keys()) + dir(type(self)) + dir(self._meshing))
        )

    def __call__(self):
        return self._meshing()
