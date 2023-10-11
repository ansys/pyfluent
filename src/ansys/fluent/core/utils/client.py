from contextlib import AbstractContextManager
import os
from typing import Optional

import requests


class Client(AbstractContextManager):
    """Client class for the go-simple-upload-server.

    https://github.com/mayth/go-simple-upload-server#go-simple-upload-server
    """

    def __init__(self, token, url="http://localhost:25478", headers=None):
        self._session = requests.Session()
        if headers:
            self._session.headers.update(headers)
        self._repo_url = url
        self._token = token

    def __exit__(self, exc_type, exc_value, traceback):
        self._session.close()
        return False

    @property
    def url(self):
        """Returns the URL."""
        return self._repo_url

    def upload_file(self, file_path: str, remote_file_name: Optional[str] = None):
        """Uploads a file.

        Parameters
        ----------
        file_path: path of the file on the client side

        Returns
        -------
        Status code
        """
        expanded_path = os.path.expandvars(file_path)
        destination_filename = remote_file_name or os.path.basename(expanded_path)
        request_url = (
            f"{self._repo_url}/files/{destination_filename}?token={self._token}"
        )
        with open(expanded_path, "rb") as f:
            file_dict = {"file": f}
            result = self._session.put(request_url, files=file_dict)
            return str(result.status_code)
        return "500"

    def get_file(self, file_name: str, text=True):
        """Gets a file contents given its name.

        Parameters
        ----------
        file_name: Name of the file
        text: If True, the result will be a unicode text. Otherwise it will be the raw bytes

        Returns
        -------
        File content
        """
        request_url = f"{self._repo_url}/files/{file_name}?token={self._token}"
        result = self._session.get(request_url)

        if text:
            return str(result.text)
        else:
            return result.content

    def download_file(self, file_name: str, local_path: str):
        """Downloads a file from a remote repository by its name.

        Parameters
        ----------
        file_name: Name of the file to download
        local_path: Local destination path

        Returns
        -------
        Downloaded file path
        """
        local = os.path.join(local_path, file_name)
        os.makedirs(local_path, exist_ok=True)
        with open(local, "wb") as f:
            f.write(self.get_file(file_name, text=False))

        return local

    def file_exist(self, file_name: str):
        """Check that a file exists on the server.

        Parameters
        ----------
        file_name: Name of the file to check

        Returns
        -------
        True if the file exists, False otherwise.
        """
        request_url = f"{self._repo_url}/files/{file_name}?token={self._token}"
        result = self._session.head(request_url)
        return result.ok
