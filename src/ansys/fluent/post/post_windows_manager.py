"""Module providing PostWindow and PostWindowManager abstract classes.

PostWindowManager is container for PostWindow.
"""
from abc import ABCMeta, abstractmethod
from typing import List, Optional, Union

from ansys.fluent.post.post_object_defns import GraphicsDefn, PlotDefn


class PostWindow:
    """Abstract class for post window."""

    @abstractmethod
    def plot(self):
        """Draw plot."""
        pass


class PostWindowsManager(metaclass=ABCMeta):
    """Abstract class for post windows management."""

    @abstractmethod
    def open_window(self, window_id: Optional[str] = None) -> str:
        """Open new window.

        Parameters
        ----------
        window_id : str, optional
            Id for new window. If not specified unique id is used.

        Returns
        -------
        str
            Window id.
        """
        pass

    @abstractmethod
    def set_object_for_window(
        self, object: Union[GraphicsDefn, PlotDefn], window_id: str
    ) -> None:
        """Associate post object with running window instance.

        Parameters
        ----------
        object : Union[GraphicsDefn, PlotDefn]
            Post object to associate with window.

        window_id : str
            Window id to associate.

        Raises
        ------
        RuntimeError
            If window does not support object.
        """
        pass

    @abstractmethod
    def plot(
        self,
        object: Union[GraphicsDefn, PlotDefn],
        window_id: Optional[str] = None,
    ) -> None:
        """Draw plot.

        Parameters
        ----------
        object: Union[GraphicsDefn, PlotDefn]
            Object to plot.

        window_id : str, optional
            Window id for plot. If not specified unique id is used.

        Raises
        ------
        RuntimeError
            If window does not support object.
        """
        pass

    @abstractmethod
    def save_graphic(
        self,
        window_id: str,
        format: str,
    ) -> None:
        """Save graphics.

        Parameters
        ----------
        window_id : str
            Window id for which graphic should be saved.
        format : str
            Graphic format.

        Raises
        ------
        ValueError
            If window does not support specified format.
        """
        pass

    @abstractmethod
    def refresh_windows(
        self,
        session_id: Optional[str] = "",
        windows_id: Optional[List[str]] = [],
    ) -> None:
        """Refresh windows.

        Parameters
        ----------
        session_id : str, optional
           Session id to refresh. If specified, all windows which belong to
           specified session will be refreshed. Otherwise windows for all
           sessions will be refreshed.

        windows_id : List[str], optional
            Windows id to refresh. If not specified, all windows will be
            refreshed.
        """
        pass

    @abstractmethod
    def animate_windows(
        self,
        session_id: Optional[str] = "",
        windows_id: Optional[List[str]] = [],
    ) -> None:
        """Animate windows.

        Parameters
        ----------
        session_id : str, optional
           Session id to animate. If specified, animation will be created
           for windows which belong to specified session. Otherwise
           animation will be created for all windows.

        windows_id : List[str], optional
            Windows id to animate. If not specified, animation will be
            created for all windows.

        Raises
        ------
        NotImplementedError
            If not implemented.
        """
        pass

    @abstractmethod
    def close_windows(
        self,
        session_id: Optional[str] = "",
        windows_id: Optional[List[str]] = [],
    ) -> None:
        """Close windows.

        Parameters
        ----------
        session_id : str, optional
           Session id to close. If specified, windows which belong to
           specified session will be closed. Otherwise windows for all
           sessions will be closed.

        windows_id : List[str], optional
            Windows id to close. If not specified, all windows will be
            closed.
        """
        pass
