"""Module providing components for PyFluent.

Componnets are the building block of PyFluent ui. PyFluent ui can be
created/customized by rendering different components as per the requirement.

Following is the list of supported components:
- Outline
- LocalPropertyEditor
- SettingsPropertyEditor
- MonitorWindow
- GraphicsWindow
- PlotWindow
- ProgressBar

Each component's instance must be initialized before it is rendered. Initialization
takes user id, session id as compulsory and index as optional argument. Multiple
instances of the same component can be created by passing different indices during
initialization.

Index also allows to link different components together. For example GraphicsWindow
and PlotWindow should update when plot or display is triggered by
LocalPropertyEditor. This linking can be achieved by component's index.

Example
-------
>>> from ansys.fluent.gui.components import (
>>>    GraphicsWindow,
>>>    LocalPropertyEditor,
>>>    SettingsPropertyEditor,
>>>)

Instantiate the components.

>>> settings_editor1=SettingsPropertyEditor("session-1", "user-1")
>>> settings_editor2=SettingsPropertyEditor("session-1", "user-1", 1)
>>> local_editor=LocalPropertyEditor("session-1", "user-1", 1)
>>> graphics=GraphicsWindow("session-1", "user-1", 1)

Once instantiated, component can be rendered by invoking __call__ method. It takes
component's properties as arguments.

>>> settings_editor1("setup/models/viscous")
>>> settings_editor2("setup/models/multiphase")
>>> local_editor("Contour")
>>> graphics()

local_editor and  graphics have same index so these two are automatically linked.
So any display or plot action on local_editor will update the graphics component.
"""

from ansys.fluent.gui.components.objects_handle import (  # noqa: F401
    LOCAL_ID,
    SETTINGS_ID,
)
from ansys.fluent.gui.components.outline import Outline  # noqa: F401
from ansys.fluent.gui.components.post_windows import (  # noqa: F401
    GraphicsWindow,
    MonitorWindow,
    PlotWindow,
)
from ansys.fluent.gui.components.progress_bar import ProgressBar  # noqa: F401
from ansys.fluent.gui.components.property_editors import (  # noqa: F401
    LocalPropertyEditor,
    SettingsPropertyEditor,
)
from ansys.fluent.gui.components.sessions_handle import SessionsHandle  # noqa: F401
from ansys.fluent.gui.components.state_manager import StateManager  # noqa: F401
