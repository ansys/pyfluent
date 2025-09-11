# Copyright (C) 2021 - 2025 ANSYS, Inc. and/or its affiliates.
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

"""Public exposure of ui UI for PyFluent."""


def in_jupyter():
    """Checks if the library is being used in a Jupyter environment."""
    try:
        from IPython import get_ipython

        return "IPKernelApp" in get_ipython().config
    except (ImportError, AttributeError):
        return False


if in_jupyter():
    from ansys.fluent.core.ui.jupyter_ui import (
        set_auto_refresh,
        settings_ui,
    )
else:
    from ansys.fluent.core.ui.standalone_web_ui import (  # noqa: F401
        build_settings_view,
        set_auto_refresh,
    )


def ui(settings_obj):
    """PyFluent ui UI wrapper."""
    if in_jupyter():
        import IPython
        from IPython.display import display

        if hasattr(IPython, "get_ipython") and "ZMQInteractiveShell" in str(
            type(IPython.get_ipython())
        ):
            display(settings_ui(settings_obj))
    else:
        import panel as pn

        pn.extension()
        view = build_settings_view(settings_obj)
        view.servable()
        pn.serve(view)
