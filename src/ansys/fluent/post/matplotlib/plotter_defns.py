"""Module providing matplotlib plotter functionality."""

from typing import List, Optional

import matplotlib.pyplot as plt
import numpy as np


class Plotter:
    """Class for matplotlib plotter."""

    def __init__(
        self,
        window_id: str,
        curves: Optional[List[str]] = [],
        title: Optional[str] = "XY Plot",
        xlabel: Optional[str] = "position",
        ylabel: Optional[str] = "",
        remote_process: Optional[bool] = False,
    ):
        """Instantiate a matplotlib plotter.

        Parameters
        ----------
        window_id : str
            Window id.
        curves : List[str], optional
            List of curves name.
        title : str, optional
            Plot title.
        xlabel : str, optional
            X axis label.
        ylabel : str, optional
            Y axis label.
        figure : str, optional
            Matplot lib figure.
        axis : str, optional
            Subplot indices.
        remote_process: bool, optional
            Is remote process.
        """
        self._curves = curves
        self._title = title
        self._xlabel = xlabel
        self._ylabel = ylabel
        self._window_id = window_id
        self._min_y = None
        self._max_y = None
        self._min_x = None
        self._max_x = None
        self._yscale = None
        self._data = {}
        self._closed = False
        self._visible = False
        if not remote_process:
            self.fig = plt.figure(num=self._window_id)
            self.ax = self.fig.add_subplot(111)

    def plot(self, data: dict) -> None:
        """Draw plot in window.

        Parameters
        ----------
        data : dict
            Data to plot. Data consists the list of x and y
            values for each curve.
        """
        if not data:
            return

        for curve in data:
            min_y_value = np.amin(data[curve]["yvalues"])
            max_y_value = np.amax(data[curve]["yvalues"])
            min_x_value = np.amin(data[curve]["xvalues"])
            max_x_value = np.amax(data[curve]["xvalues"])
            self._data[curve]["xvalues"] = data[curve]["xvalues"].tolist()
            self._data[curve]["yvalues"] = data[curve]["yvalues"].tolist()
            self._min_y = min(self._min_y, min_y_value) if self._min_y else min_y_value
            self._max_y = max(self._max_y, max_y_value) if self._max_y else max_y_value
            self._min_x = min(self._min_x, min_x_value) if self._min_x else min_x_value
            self._max_x = max(self._max_x, max_x_value) if self._max_x else max_x_value

        curve_lines = self.ax.lines
        for curve, curve_line in zip(self._curves, curve_lines):
            curve_line.set_data(
                self._data[curve]["xvalues"], self._data[curve]["yvalues"]
            )
        if self._max_x > self._min_x:
            self.ax.set_xlim(self._min_x, self._max_x)
        y_range = self._max_y - self._min_y
        if self._yscale == "log":
            y_range = 0
        self.ax.set_ylim(self._min_y - y_range * 0.2, self._max_y + y_range * 0.2)

        if not self._visible:
            self._visible = True
            plt.show()

    def close(self):
        """Close window."""
        plt.close(self.fig)
        self._closed = True

    def is_closed(self):
        """Check if window is closed."""
        return self._closed

    def save_graphic(self, file_name: str):
        """Save graphics.

        Parameters
        ----------
        file_name : str
            File name to save graphic.
        """
        plt.savefig(file_name)

    def set_properties(self, properties: dict):
        """Set plot properties.

        Parameters
        ----------
        properties : dict
            Plot properties i.e. curves, title, xlabel and ylabel.
        """
        self._curves = properties.get("curves", self._curves)
        self._title = properties.get("title", self._title)
        self._xlabel = properties.get("xlabel", self._xlabel)
        self._ylabel = properties.get("ylabel", self._ylabel)
        self._yscale = properties.get("yscale", self._yscale)
        self._data = {}
        self._min_y = None
        self._max_y = None
        self._min_x = None
        self._max_x = None
        self._reset()

    def __call__(self):
        """Reset and show plot."""
        self._reset()
        self._visible = True
        plt.show()

    # private methods
    def _reset(self):
        plt.figure(self.fig.number)
        self.ax.cla()
        if self._yscale:
            self.ax.set_yscale(self._yscale)
        for curve_name in self._curves:
            self._data[curve_name] = {}
            self._data[curve_name]["xvalues"] = []
            self._data[curve_name]["yvalues"] = []
            self.ax.plot([], [], label=curve_name)
        self.fig.canvas.set_window_title("PyFluent [" + self._window_id + "]")
        plt.title(self._title)
        plt.xlabel(self._xlabel)
        plt.ylabel(self._ylabel)
        plt.legend(loc="upper right")


class ProcessPlotter(Plotter):
    """Class for matplotlib process plotter.

    Opens matplotlib window in a separate process.
    """

    def __init__(
        self,
        window_id,
        curves_name=[],
        title="XY Plot",
        xlabel="position",
        ylabel="",
    ):
        """Instantiate a matplotlib process plotter.

        Parameters
        ----------
        window_id : str
            Window id.
        curves : List[str], optional
            List of curves name.
        title : str, optional
            Plot title.
        xlabel : str, optional
            X axis label.
        ylabel : str, optional
            Y axis label.
        """
        super().__init__(window_id, curves_name, title, xlabel, ylabel, True)

    def _call_back(self):
        try:
            while self.pipe.poll():
                data = self.pipe.recv()
                if data is None:
                    self.close()
                    return False
                elif data and isinstance(data, dict):
                    if "properties" in data:
                        properties = data["properties"]
                        self.set_properties(properties)
                    elif "save_graphic" in data:
                        name = data["save_graphic"]
                        self.save_graphic(name)
                    else:
                        self.plot(data)
            self.fig.canvas.draw()
        except BrokenPipeError:
            self.close()
        return True

    def __call__(self, pipe):
        """Reset and show plot."""
        self.pipe = pipe
        self.fig = plt.figure(num=self._window_id)
        self.ax = self.fig.add_subplot(111)
        self._reset()
        timer = self.fig.canvas.new_timer(interval=10)
        timer.add_callback(self._call_back)
        timer.start()
        self._visible = True
        plt.show()
