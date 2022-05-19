"""Module providing component abstract base class."""
from abc import ABCMeta, abstractmethod


class ComponentBase(metaclass=ABCMeta):
    """Abstract class for components."""

    @abstractmethod
    def render(self) -> object:
        """Render component.

        Parameters
        ----------
        None

        Returns
        -------
        object
            Component.
        """
        pass

    @abstractmethod
    def __call__(self, *args, **kwargs) -> object:
        """Render customized component.

        It takes component properties and render customized component within a container.
        Instead of render this method should be used to render a component.

        Parameters
        ----------
        Component Properties.

        Returns
        -------
        object
            Customized component.
        """
        pass
