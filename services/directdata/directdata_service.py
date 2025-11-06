import requests
from typing import Dict, Optional, Any, List


class DirectDataService:
    """
    Service class for handling Direct Data API operations with Veeva Vault.

    Direct Data API provides high-speed read-only data access to Vault.
    This service allows you to retrieve available Direct Data files and download them.

    Note: Direct Data API is not enabled by default. You must contact Veeva Support to enable it in your Vault.
    Certain permissions are required for the Vault integration user to use these endpoints.
    """

    def __init__(self, client):
        """
        Initialize with a VaultClient instance

        Args:
            client: An initialized VaultClient instance
        """
        self.client = client

    def retrieve_available_direct_data_files(
        self,
        extract_type: Optional[str] = None,
        start_time: Optional[str] = None,
        stop_time: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Retrieves a list of all Direct Data files available for download.

        Args:
            extract_type: Optional. The Direct Data file type: incremental_directdata,
                          full_directdata, or log_directdata. If omitted, returns all files.
            start_time: Optional. Specify a time in YYYY-MM-DDTHH:MM:SSZ format.
                        If omitted, defaults to the Vault's creation date and time.
                        All Full files have a start time of 2000-01-01T00:00:00Z.
            stop_time: Optional. Specify a time in YYYY-MM-DDTHH:MM:SSZ format.
                       If omitted, defaults to today's date and current time.

        Returns:
            dict: Response containing list of available Direct Data files and their metadata.
                  On SUCCESS, Vault lists all Direct Data files available for download including:
                  - name: The name of the Direct Data file, excluding the .gzip extension
                  - filename: The name of the Direct Data .gzip file
                  - extract_type: The Direct Data file type (incremental_directdata, full_directdata, or log_directdata)
                  - start_time: The start time in YYYY-MM-DDTHH:MM:SSZ format
                  - stop_time: The stop time in YYYY-MM-DDTHH:MM:SSZ format
                  - record_count: The number of records for a given extract
                  - size: The size of the Direct Data file in bytes
                  - fileparts: The number of file parts for a given Direct Data file
                  - filepart_details: A list of all file parts and their metadata
        """
        url = f"api/{self.client.LatestAPIversion}/services/directdata/files"

        params = {}
        if extract_type:
            params["extract_type"] = extract_type
        if start_time:
            params["start_time"] = start_time
        if stop_time:
            params["stop_time"] = stop_time

        headers = {"Accept": "application/json"}

        return self.client.api_call(url, method="GET", headers=headers, params=params)

    def download_direct_data_file(self, file_name: str) -> bytes:
        """
        Downloads a Direct Data file.

        Args:
            file_name: The name of the Direct Data file part. Obtain this from the
                      retrieve_available_direct_data_files request. For example, 146478-20240213-0000-F.001.

        Returns:
            bytes: The binary content of the direct data file.
                  The file is named according to the format: {vaultid}-{date}-{stoptime}-{type}.tar.gz.{filepart}

        Note:
            Until the first Full file is generated, no Incremental files are available for download.
            The API may return a standard error if an Incremental file is unavailable for download:
            FAILURE: Initial file being generated. Please check again later.
        """
        url = (
            f"api/{self.client.LatestAPIversion}/services/directdata/files/{file_name}"
        )

        # For binary download, we need to make a custom request outside of the api_call method
        # since we don't want JSON parsing
        full_url = f"{self.client.vaultURL}/{url}"
        auth_headers = {
            "Authorization": self.client.sessionId,
            "Accept": "application/octet-stream",
        }

        response = requests.get(full_url, headers=auth_headers)
        response.raise_for_status()

        return response.content
