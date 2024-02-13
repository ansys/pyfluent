import os
from typing import Any, Callable, Optional, Union  # noqa: F401

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
        return pypim.is_configured()

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

    def upload_file(
        self, file_name: Union[list[str], str], on_uploaded: Optional[Callable] = None
    ):
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
        files = [file_name] if isinstance(file_name, str) else file_name
        if self.is_configured():
            for file in files:
                if os.path.isfile(file):
                    if not self.file_service.file_exist(os.path.basename(file)):
                        self.upload(file)
                elif not self.file_service.file_exist(os.path.basename(file)):
                    raise FileNotFoundError(f"{file} does not exist.")
        if on_uploaded:
            for file in files:
                on_uploaded(os.path.basename(file) if self.is_configured() else file)

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
        if not self.is_configured():
            raise PyPIMConfigurationError()
        elif self.file_service:
            if self.file_service.file_exist(file_name):
                self.file_service.download_file(file_name, local_file_name)
            else:
                raise FileNotFoundError("Remote file does not exist.")

    def download_file(
        self,
        file_name: Union[list[str], str],
        before_downloaded: Optional[Callable] = None,
    ):
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
        files = [file_name] if isinstance(file_name, str) else file_name
        for file in files:
            if before_downloaded:
                before_downloaded(
                    os.path.basename(file) if self.is_configured() else file
                )
        if self.is_configured():
            for file in files:
                if os.path.isfile(file):
                    print(f"\nFile already exists. File path:\n{file}\n")
                else:
                    self.download(os.path.basename(file), local_file_name=".")


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
        self._transfer_service.upload_file(file_name=file_name, on_uploaded=on_uploaded)

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
        self._transfer_service.download_file(
            file_name=file_name, before_downloaded=before_downloaded
        )

    def __bool__(self):
        return (
            self._transfer_service.is_configured() if self._transfer_service else False
        )


class TransferRequestRecorder:
    def __init__(self):
        self.uploaded_files = list()
        self.downloaded_files = list()

    def uploads(self):
        return self.uploaded_files

    def downloads(self):
        return self.downloaded_files

    def upload_file(self, file_name: str, on_uploaded: Optional[Callable] = None):
        self.uploaded_files.append(file_name)

    def download_file(
        self, file_name: str, before_downloaded: Optional[Callable] = None
    ):
        self.downloaded_files.append(file_name)

    def is_configured(self):
        return True
