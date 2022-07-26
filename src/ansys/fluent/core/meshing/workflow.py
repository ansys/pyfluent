

def new_command_for_task(task, meshing):

    class NewCommandError(Exception):
        def __init__(self, task_name):
            super().__init__(
                f"Could not create command for meshing task {task_name}")


    task_cmd_name = task.CommandName()
    cmd_creator = getattr(meshing, task_cmd_name)
    if cmd_creator:
        new_cmd = cmd_creator.new()
        if new_cmd:
            return new_cmd
    raise NewCommandError(task._name_())


class MeshingWorkflow:

    class Task:

        class Arguments:

            def __init__(self, task):
                self._task = task
                self._args = task.Arguments
                
            def __getattr__(self, attr):
                return getattr(self._args, attr)

            def get_expanded_state(self):
                return self._task.get_expanded_arg_state()


        def __init__(self, meshing, name):
            self._workflow = meshing._workflow
            self._meshing = meshing._meshing
            self._task = self._workflow.TaskObject[name]
            self._cmd = None

        def get_expanded_arg_state(self):
            return self._command().get_state()

        def _command(self):
            if not self._cmd:
                self._cmd = new_command_for_task(self._task, self._meshing)
            return self._cmd

        def __getattr__(self, attr):
            return getattr(self._task, attr)


    def __init__(self, meshing):
        self._workflow = meshing.workflow
        self._meshing = meshing.meshing

    def task(self, name):
        return MeshingWorkflow.Task(self, name)
    
    def __getattr__(self, attr):
        return getattr(self._workflow, attr)
