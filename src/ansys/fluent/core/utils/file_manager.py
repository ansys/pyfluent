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
        Upload a file on the server.

    is_file(
        file_name
        )
        Check if a file available on the server.

    _get_file_contents(
        file_name, is_unicode_text
        )
        Get file contents.

    download(
        file_name, local_file_path
        )
        Download a file from the server.
    """

    def __init__(self, url):
        self.session = requests.Session()
        self.url = url

    def __exit__(self):
        self.session.close()

    def upload(self, file_path: str, remote_file_name: Optional[str] = None):
        """Uploads a file on the server.

        Parameters
        ----------
        file_path: local file path
        remote_file_name: file name on server
        Returns
        -------
        Status code
        """
        path = os.path.expandvars(file_path)
        filename = remote_file_name or os.path.basename(path)
        temp_url = f"{self.url}/{filename}?token={'temp_token'}"
        with open(path, "rb") as file:
            file_data = {"file": file}
            upload = self.session.put(temp_url, files=file_data)
            return str(upload.status_code)
        return "0"

    def is_file(self, file_name: str):
        """Check if the file exists on the server.

        Parameters
        ----------
        file_name: File name to check

        Returns
        -------
        True if the file exists, False otherwise.
        """
        temp_url = f"{self.url}/{file_name}?token={'temp_token'}"
        file_status = self.session.head(temp_url)
        return file_status.ok

    def _get_file_contents(self, file_name: str, is_unicode_text):
        """Gets the file contents.

        Parameters
        ----------
        file_name: File name
        is_unicode_text: Returns unicode text if True, else returns raw bytes

        Returns
        -------
        File contents.
        """
        temp_url = f"{self.url}/{file_name}?token={'temp_token'}"
        contents = self.session.get(temp_url)

        if is_unicode_text:
            return str(contents.text)
        else:
            return contents.content

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
            file.write(self._get_file_contents(file_name, False))

        return local_path
