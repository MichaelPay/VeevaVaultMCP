class CustomPagesService:
    """
    Service class for managing Custom Pages in Veeva Vault.

    This service provides methods to manage the client code for Custom Pages using
    a client code distribution. The client code distribution contains:
    - The client code that defines how Custom Pages display in the Vault UI
    - Metadata that describes the distribution, placed in a manifest file (distribution-manifest.json)
      in the distribution's root directory.

    Client code distributions are uploaded to and downloaded from Vault as a ZIP file.
    """

    def __init__(self, client):
        """
        Initialize with a VaultClient instance

        Args:
            client: An initialized VaultClient instance for API communication
        """
        self.client = client

    def retrieve_all_client_code_distributions(self):
        """
        Retrieve a list of all client code distributions in the Vault and their metadata.

        This endpoint does not retrieve the contents of distribution manifest files.

        Corresponds to GET /api/{version}/uicode/distributions

        Returns:
            dict: The JSON response containing all client code distributions in the Vault with metadata:
                - name: The name of the client code distribution.
                - checksum: A unique string used to identify the distribution.
                - size: The size of the unzipped client code distribution in bytes.
        """
        url = f"api/{self.client.LatestAPIversion}/uicode/distributions"
        return self.client.api_call(url)

    def retrieve_client_code_distribution(self, distribution_name):
        """
        Retrieve metadata for a specific client code distribution.

        Gets detailed metadata for a specific client code distribution, including its name,
        size, and details from the uploaded distribution-manifest.json file.

        Corresponds to GET /api/{version}/uicode/distributions/{distribution_name}

        Args:
            distribution_name (str): The name attribute of the client code distribution to retrieve.

        Returns:
            dict: The JSON response containing metadata for the specified distribution:
                - name: The name of the client code distribution.
                - checksum: A unique string used to identify the distribution.
                - size: The size of the unzipped client code distribution in bytes.
                - pages: The pages listed in the distribution-manifest.json file.
                        For each page, this includes the name, file, and export values.
                - stylesheets: The optional list of stylesheet paths from the distribution-manifest.json file.
                - importmap: The optional importmap included in the distribution-manifest.json file.
        """
        url = f"api/{self.client.LatestAPIversion}/uicode/distributions/{distribution_name}"
        return self.client.api_call(url)

    def download_client_code_distribution(self, distribution_name):
        """
        Download a ZIP file containing the client code distribution directory.

        Downloads a ZIP containing the client code files and the distribution manifest
        (distribution-manifest.json).

        Corresponds to GET /api/{version}/uicode/distributions/{distribution_name}/code

        Args:
            distribution_name (str): The name attribute of the client code distribution to download.

        Returns:
            bytes: The ZIP file contents of the client code distribution.
                  The Content-Type is set to application/zip;charset=UTF-8.
                  The Content-Disposition header contains a filename component which can be used
                  when naming the local file. The filename is {distribution_name}.zip.
        """
        url = f"api/{self.client.LatestAPIversion}/uicode/distributions/{distribution_name}/code"

        # Set raw_response=True to get the binary content directly
        return self.client.api_call(url, raw_response=True)

    def upload_client_code_distribution(self, zip_file_path):
        """
        Add or replace client code in Vault by uploading a ZIP file of the client code distribution.

        Vault unpacks and compares the uploaded distribution with other distributions in the Vault and:
        - Adds the distribution if the distribution name is new.
        - Replaces a distribution if it has the same name and the client code filenames or contents are different.
        - Makes no changes if the distribution name exists and the code is the same.

        Corresponds to POST /api/{version}/uicode/distributions/

        Args:
            zip_file_path (str): The file path to the ZIP file containing the client code distribution.
                                The maximum allowed total file size for all distributions in a Vault is 50 MB.

        Returns:
            dict: The JSON response containing:
                - name: The name of the distribution as specified in the manifest file.
                - updateType: Whether the distribution was added (ADDED), replaced (MODIFIED),
                              or left unchanged (NO_CHANGE).
                - checksum: A unique string used to identify the distribution and whether the contents have changed.
        """
        url = f"api/{self.client.LatestAPIversion}/uicode/distributions/"

        # Prepare file for upload
        files = {"file": open(zip_file_path, "rb")}

        return self.client.api_call(url, method="POST", files=files)

    def delete_client_code_distribution(self, distribution_name):
        """
        Delete a specific client code distribution.

        To delete a distribution, you must first remove all Page components associated with it from your Vault.
        To delete a single file from an existing distribution, re-package the distribution without the file
        and re-upload the distribution to Vault.

        Corresponds to DELETE /api/{version}/uicode/distributions/{distribution_name}

        Args:
            distribution_name (str): The name attribute of the client code distribution to delete.

        Returns:
            dict: The JSON response containing:
                - responseStatus: "SUCCESS" if the deletion was successful
        """
        url = f"api/{self.client.LatestAPIversion}/uicode/distributions/{distribution_name}"

        return self.client.api_call(url, method="DELETE")
