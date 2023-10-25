import os
from typing import Any, Callable, Optional  # noqa: F401

import ansys.platform.instancemanagement as pypim


class FileTransferService:
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

    def __init__(self, pim_instance):
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

    def _upload_download_helper(
        self,
        is_upload: bool,
        file_name: Optional[str] = None,
        remote_file_name: Optional[str] = None,
        local_file_name: Optional[str] = None,
    ):
        """Uploads and downloads a file.

        Parameters
        ----------
        is_upload : bool
            True if we want to upload file, False otherwise.
        file_name : str
            file name
        remote_file_name : str, optional
            remote file name, by default None
        local_file_name : str, optional
            local file name, by default None
        Raises
        ------
        FileNotFoundError
            If the file does not exist.
        """
        if self.file_service:
            if is_upload:
                if os.path.isfile(file_name):
                    expanded_file_path = os.path.expandvars(file_name)
                    upload_file_name = remote_file_name or os.path.basename(
                        expanded_file_path
                    )
                    self.file_service.upload_file(expanded_file_path, upload_file_name)
                else:
                    raise FileNotFoundError(f"{file_name} does not exist.")
            else:
                if self.file_service.file_exist(file_name):
                    self.file_service.download_file(file_name, local_file_name)
                else:
                    raise FileNotFoundError("Remote file does not exist.")

    def upload(self, file_name: str, remote_file_name: Optional[str] = None):
        """Uploads a file on the server.

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
        """
        self._upload_download_helper(
            is_upload=True, file_name=file_name, remote_file_name=remote_file_name
        )

    def download(self, file_name: str, local_file_name: Optional[str] = None):
        """Downloads a file from the server.

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
        """
        self._upload_download_helper(
            is_upload=False, file_name=file_name, local_file_name=local_file_name
        )

    def _pypim_upload(self, file_name: str, on_uploaded: Optional[Any] = None):
        """Uploads a file if not available on the server.

        Parameters
        ----------
        file_name : str
            File name
        on_uploaded: Callable[str]
            Read a file.
        Raises
        ------
        FileNotFoundError
            If a file does not exist.
        """
        if pypim.is_configured():
            if os.path.isfile(file_name):
                if not self.file_service.file_exist(os.path.basename(file_name)):
                    self.upload(file_name)
            elif not self.file_service.file_exist(os.path.basename(file_name)):
                raise FileNotFoundError(f"{file_name} does not exist.")
        if on_uploaded:
            on_uploaded(os.path.basename(file_name))

    def _pypim_download(self, file_name: str, on_uploaded: Optional[Any] = None):
        """Downloads a file from the server.

        Parameters
        ----------
        file_name : str
            File name
        on_uploaded: Callable[str]
            Write a file.
        """
        if on_uploaded:
            on_uploaded(os.path.basename(file_name))
        if pypim.is_configured():
            if os.path.isfile(file_name):
                print(f"\nFile already exists. File path:\n{file_name}\n")
            else:
                self.download(os.path.basename(file_name), ".")
