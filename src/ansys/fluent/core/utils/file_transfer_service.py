"""Provides a module for file transfer service."""

import os
from typing import Any, Callable, Optional, Union  # noqa: F401

import ansys.platform.instancemanagement as pypim


class PyPIMConfigurationError(ConnectionError):
    """Raised when `PyPIM<https://pypim.docs.pyansys.com/version/stable/>` is not configured."""

    def __init__(self):
        super().__init__("PyPIM is not configured.")


class PimFileTransferService:
    """Provides a file transfer service based on ``PyPIM<https://pypim.docs.pyansys.com/version/stable/>`` and ``simple_upload_server()``.

    Attributes
    ----------
    pim_instance: PIM instance
        Instance of PIM which supports upload server services.

    file_service: Client instance
        Instance of Client which supports upload and download methods.

    Methods
    -------
    upload(
        file_name, remote_file_name
        )
        Upload a file to the server.

    download(
        file_name, local_directory
        )
        Download a file from the server.
    """

    def __init__(self, pim_instance: Optional[Any] = None):
        self.pim_instance = pim_instance
        self.upload_server = None
        self.file_service = None
        try:
            if "http-simple-upload-server" in self.pim_instance.services:
                self.upload_server = self.pim_instance.services[
                    "http-simple-upload-server"
                ]
            elif "grpc" in self.pim_instance.services:
                self.upload_server = self.pim_instance.services["grpc"]
        except (AttributeError, KeyError):
            pass
        else:
            try:
                from simple_upload_server.client import Client

                self.file_service = Client(
                    token="token",
                    url=self.upload_server.uri,
                    headers=self.upload_server.headers,
                )
            except ModuleNotFoundError:
                pass

    @property
    def pim_service(self):
        """PIM file transfer service."""
        return self.file_service

    def is_configured(self):
        """Check pypim configuration."""
        return pypim.is_configured()

    def upload_file(self, file_name: str, remote_file_name: Optional[str] = None):
        """Upload a file to the server supported by `PyPIM<https://pypim.docs.pyansys.com/version/stable/>`.

        Parameters
        ----------
        file_name : str
            file name
        remote_file_name : str, optional
            remote file name, by default None
        Raises
        ------
        FileNotFoundError
            If the file does not exist.
        PyPIMConfigurationError
            If PyPIM is not configured.
        """
        if not self.is_configured():
            raise PyPIMConfigurationError()
        elif self.file_service:
            if os.path.isfile(file_name):
                expanded_file_path = os.path.expandvars(file_name)
                upload_file_name = remote_file_name or os.path.basename(
                    expanded_file_path
                )
                self.file_service.upload_file(expanded_file_path, upload_file_name)
            else:
                raise FileNotFoundError(f"{file_name} does not exist.")

    def upload(self, file_name: Union[list[str], str]):
        """Upload a file to the server.

        Parameters
        ----------
        file_name : str
            File name
        Raises
        ------
        FileNotFoundError
            If a file does not exist.
        """
        files = [file_name] if isinstance(file_name, str) else file_name
        if self.is_configured():
            for file in files:
                if os.path.isfile(file):
                    if not self.file_service.file_exist(os.path.basename(file)):
                        self.upload_file(file_name=file)
                elif not self.file_service.file_exist(os.path.basename(file)):
                    raise FileNotFoundError(f"{file} does not exist.")

    def download_file(self, file_name: str, local_directory: Optional[str] = None):
        """Download a file from the server supported by `PyPIM<https://pypim.docs.pyansys.com/version/stable/>`.

        Parameters
        ----------
        file_name : str
            file name
        local_directory : str, optional
            local directory, by default None

        Raises
        ------
        FileNotFoundError
            If the remote file does not exist.
        PyPIMConfigurationError
            If PyPIM is not configured.
        """
        if not self.is_configured():
            raise PyPIMConfigurationError()
        elif self.file_service:
            if self.file_service.file_exist(file_name):
                self.file_service.download_file(file_name, local_directory)
            else:
                raise FileNotFoundError("Remote file does not exist.")

    def download(
        self,
        file_name: Union[list[str], str],
    ):
        """Download a file from the server.

        Parameters
        ----------
        file_name : str
            File name
        """
        files = [file_name] if isinstance(file_name, str) else file_name
        if self.is_configured():
            for file in files:
                if os.path.isfile(file):
                    print(f"\nFile already exists. File path:\n{file}\n")
                else:
                    self.download_file(
                        file_name=os.path.basename(file), local_directory="."
                    )

    def __call__(self, pim_instance: Optional[Any] = None):
        self.pim_instance = pim_instance
