from contextlib import AbstractContextManager
import os
from typing import Optional

import requests


class FileManager(AbstractContextManager):
    """Instantiates a file uploader and downloader to have a seamless file
    reading and writing.

    Attributes
    ----------
    url: server url
        Server url to upload and download files.

    Methods
    -------
    upload(
        file_path, remote_file_name
        )
        Upload a file to the server.

    file_exist(
        file_name
        )
        Check that a file exists on the server.

    download(
        file_name, local_file_path
        )
        Download a file from the server.
    """

    def __init__(self, url):
        self.session = requests.Session()
        self.url = url

    def __exit__(self, exc_type, exc_value, traceback):
        self.session.close()
        return False

    def upload(self, file_path: str, remote_file_name: Optional[str] = None):
        """Uploads a file on the server.

        Parameters
        ----------
        file_path: local file path

        Returns
        -------
        Status code
        """
        path = os.path.expandvars(file_path)
        filename = remote_file_name or os.path.basename(path)
        request_url = f"{self.url}/{filename}?token={'temp_token'}"
        with open(path, "rb") as file:
            file_dict = {"file": file}
            result = self.session.put(request_url, files=file_dict)
            return str(result.status_code)
        return "0"

    def file_exist(self, file_name):
        """Check that a file exists on the server.

        Parameters
        ----------
        file_name: File name to check

        Returns
        -------
        True if the file exists, False otherwise.
        """
        request_url = f"{self.url}/{file_name}?token={'temp_token'}"
        result = self.session.head(request_url)
        return result.ok

    def download(self, file_name: str, local_file_path: Optional[str] = None):
        """Downloads a file from the server.

        Parameters
        ----------
        file_name: File name to download
        local_file_path: Local file path

        Returns
        -------
        Downloaded file path
        """
        local_path = os.path.join(local_file_path, file_name)
        os.makedirs(local_file_path, exist_ok=True)
        with open(local_path, "wb") as file:
            file.write(self.get_file(file_name, text=False))

        return local_path
