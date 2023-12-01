import os
from typing import Any, Callable, Optional  # noqa: F401

import ansys.platform.instancemanagement as pypim


class PyPIMConfigurationError(ConnectionError):
    """Provides the error when `PyPIM<https://pypim.docs.pyansys.com/version/stable/>` is not configured."""

    def __init__(self):
        super().__init__("PyPIM is not configured.")


class PimFileTransferService:
    """Instantiates a file uploader and downloader to have a seamless file reading /
    writing in the cloud particularly in Ansys lab . Here we are exposing upload and
    download methods on session objects. These would be no- ops if PyPIM is not
    configured or not authorized with the appropriate service. This will be used for
    internal purpose only.

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
        file_name, local_file_name
        )
        Download a file from the server.
    """

    def __init__(self, pim_instance: Optional[Any] = None):
        self.pim_instance = pim_instance
        self.file_service = None
        try:
            upload_server = self.pim_instance.services["http-simple-upload-server"]
        except (AttributeError, KeyError):
            pass
        else:
            from simple_upload_server.client import Client

            self.file_service = Client(
                token="token", url=upload_server.uri, headers=upload_server.headers
            )

    @property
    def pim_service(self):
        """PIM file transfer service."""
        return self.file_service

    def upload(self, file_name: str, remote_file_name: Optional[str] = None):
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
        if not pypim.is_configured():
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

    def download(self, file_name: str, local_file_name: Optional[str] = None):
        """Download a file from the server supported by `PyPIM<https://pypim.docs.pyansys.com/version/stable/>`.

        Parameters
        ----------
        file_name : str
            file name
        local_file_name : str, optional
            local file path, by default None

        Raises
        ------
        FileNotFoundError
            If the remote file does not exist.
        PyPIMConfigurationError
            If PyPIM is not configured.
        """
        if not pypim.is_configured():
            raise PyPIMConfigurationError()
        elif self.file_service:
            if self.file_service.file_exist(file_name):
                self.file_service.download_file(file_name, local_file_name)
            else:
                raise FileNotFoundError("Remote file does not exist.")


class RemoteFileHandler:
    """Uploads and downloads a file before and after performing callback operation
    respectively, if `PyPIM<https://pypim.docs.pyansys.com/version/stable/>` is
    configured.

    Attributes
    ----------
    transfer_service: Client instance
        Instance of Client which supports upload and download methods.

    Methods
    -------
    upload(
        file_name, on_uploaded
        )
        Upload a file to the server before performing callback operation.

    download(
        file_name, before_downloaded
        )
        Download a file from the server after performing callback operation.
    """

    def __init__(self, transfer_service: Optional[Any] = None):
        self._transfer_service = transfer_service

    def upload(self, file_name: str, on_uploaded: Optional[Callable] = None):
        """Upload a file if it's unavailable on the server
        supported by `PyPIM<https://pypim.docs.pyansys.com/version/stable/>`
        and performs callback operation.

        Parameters
        ----------
        file_name : str
            File name
        on_uploaded: Callable
            Read a file.
        Raises
        ------
        FileNotFoundError
            If a file does not exist.
        """
        if pypim.is_configured():
            if os.path.isfile(file_name):
                if not self._transfer_service.pim_service.file_exist(
                    os.path.basename(file_name)
                ):
                    self._transfer_service.upload(file_name)
            elif not self._transfer_service.pim_service.file_exist(
                os.path.basename(file_name)
            ):
                raise FileNotFoundError(f"{file_name} does not exist.")
        if on_uploaded:
            on_uploaded(
                os.path.basename(file_name) if pypim.is_configured() else file_name
            )

    def download(self, file_name: str, before_downloaded: Optional[Callable] = None):
        """Perform callback operation and
        downloads a file if it's available to the server supported by
        `PyPIM<https://pypim.docs.pyansys.com/version/stable/>`.

        Parameters
        ----------
        file_name : str
            File name
        before_downloaded: Callable
            Write a file.
        """
        if before_downloaded:
            before_downloaded(
                os.path.basename(file_name) if pypim.is_configured() else file_name
            )
        if pypim.is_configured():
            if os.path.isfile(file_name):
                print(f"\nFile already exists. File path:\n{file_name}\n")
            else:
                self._transfer_service.download(
                    os.path.basename(file_name), local_file_name="."
                )
