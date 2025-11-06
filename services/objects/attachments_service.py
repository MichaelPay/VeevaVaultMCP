import json
from .base_service import BaseObjectService


class ObjectAttachmentsService(BaseObjectService):
    """
    Service class for handling Veeva Vault object attachment operations.

    Object records can have attachments associated with them when the object
    is configured to allow attachments. These endpoints allow for creating,
    retrieving, updating, and deleting attachments on object records.
    """

    def determine_if_attachments_are_enabled_on_an_object(self, object_name):
        """
        Determines if attachments are enabled on a specific object.

        GET /api/{version}/metadata/vobjects/{object_name}

        Args:
            object_name (str): The value of object name__v field

        Returns:
            dict: Object metadata which includes the "allow_attachments" property and
                 "attachments" in the list of urls when attachments are enabled
        """
        url = f"api/{self.client.LatestAPIversion}/metadata/vobjects/{object_name}"

        return self.client.api_call(url)

    def retrieve_object_record_attachments(self, object_name, object_record_id):
        """
        Retrieves a list of all attachments on a specific object record.

        GET /api/{version}/vobjects/{object_name}/{object_record_id}/attachments

        Args:
            object_name (str): The object name__v field value
            object_record_id (str): The object record id field value

        Returns:
            dict: List of attachments and their details including filename, format, size,
                 md5checksum, version, creation information, and version history

        Notes:
            - Attachment versioning uses integer numbers beginning with 1 and incrementing sequentially
            - There is no concept of major or minor version numbers with attachments
        """
        url = f"api/{self.client.LatestAPIversion}/vobjects/{object_name}/{object_record_id}/attachments"

        return self.client.api_call(url)

    def retrieve_object_record_attachment_metadata(
        self, object_name, object_record_id, attachment_id
    ):
        """
        Retrieves the metadata of a specific attachment on a specific object record.

        GET /api/{version}/vobjects/{object_name}/{object_record_id}/attachments/{attachment_id}

        Args:
            object_name (str): The object name__v field value
            object_record_id (str): The object record id field value
            attachment_id (str): The attachment id field value

        Returns:
            dict: Metadata details of the specified attachment including filename, description,
                 format, size, md5checksum, version, creation information, and version history

        Notes:
            - The md5checksum__v field is calculated on the latest version of the attachment
            - If an attachment is added with the same MD5 checksum as an existing attachment,
              the new attachment is not added
        """
        url = f"api/{self.client.LatestAPIversion}/vobjects/{object_name}/{object_record_id}/attachments/{attachment_id}"

        return self.client.api_call(url)

    def retrieve_object_record_attachment_versions(
        self, object_name, object_record_id, attachment_id
    ):
        """
        Retrieves all versions of a specific attachment on a specific object record.

        GET /api/{version}/vobjects/{object_name}/{object_record_id}/attachments/{attachment_id}/versions

        Args:
            object_name (str): The object name__v field value
            object_record_id (str): The object record id field value
            attachment_id (str): The attachment id field value

        Returns:
            dict: Version details of the specified attachment, listing all available versions
                 with their version numbers and URLs
        """
        url = f"api/{self.client.LatestAPIversion}/vobjects/{object_name}/{object_record_id}/attachments/{attachment_id}/versions"

        return self.client.api_call(url)

    def retrieve_object_record_attachment_version_metadata(
        self, object_name, object_record_id, attachment_id, attachment_version
    ):
        """
        Retrieves the metadata of a specific version of an attachment on a specific object record.

        GET /api/{version}/vobjects/{object_name}/{object_record_id}/attachments/{attachment_id}/versions/{attachment_version}

        Args:
            object_name (str): The object name__v field value
            object_record_id (str): The object record id field value
            attachment_id (str): The attachment id field value
            attachment_version (str): The attachment version__v field value

        Returns:
            dict: Metadata of the specified attachment version including filename, format, size,
                 md5checksum, version, and creation information
        """
        url = f"api/{self.client.LatestAPIversion}/vobjects/{object_name}/{object_record_id}/attachments/{attachment_id}/versions/{attachment_version}"

        return self.client.api_call(url)

    def download_object_record_attachment_file(
        self, object_name, object_record_id, attachment_id, file_path
    ):
        """
        Downloads the file of a specific attachment on a specific object record.

        GET /api/{version}/vobjects/{object_name}/{object_record_id}/attachments/{attachment_id}/file

        Args:
            object_name (str): The object name__v field value
            object_record_id (str): The object record id field value
            attachment_id (str): The attachment id field value
            file_path (str): Local path where the file will be saved

        Returns:
            str: Message indicating successful download

        Notes:
            - Downloads the latest version of the specified attachment
            - The Content-Type header is set to the MIME type of the file
            - If MIME type cannot be detected, Content-Type is set to application/octet-stream
            - The Content-Disposition header contains a filename component for naming the local file
        """
        url = f"api/{self.client.LatestAPIversion}/vobjects/{object_name}/{object_record_id}/attachments/{attachment_id}/file"

        response = self.client.api_call(url, stream=True, raw_response=True)

        with open(file_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        return "File downloaded successfully"

    def download_object_record_attachment_version_file(
        self,
        object_name,
        object_record_id,
        attachment_id,
        attachment_version,
        file_path,
    ):
        """
        Downloads a specific version of an attachment file from a specific object record.

        GET /api/{version}/vobjects/{object_name}/{object_record_id}/attachments/{attachment_id}/versions/{attachment_version}/file

        Args:
            object_name (str): The object name__v field value
            object_record_id (str): The object record id field value
            attachment_id (str): The attachment id field value
            attachment_version (str): The attachment version__v field value
            file_path (str): Local path where the file will be saved

        Returns:
            str: Message indicating successful download

        Notes:
            - The file name is the same as the attachment file name
            - The Content-Type header is set to the MIME type of the file
            - If MIME type cannot be detected, Content-Type is set to application/octet-stream
            - The Content-Disposition header contains a filename component for naming the local file
        """
        url = f"api/{self.client.LatestAPIversion}/vobjects/{object_name}/{object_record_id}/attachments/{attachment_id}/versions/{attachment_version}/file"

        response = self.client.api_call(url, stream=True, raw_response=True)

        with open(file_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        return "File downloaded successfully"

    def download_all_object_record_attachment_files(
        self, object_name, object_record_id, directory_path
    ):
        """
        Downloads all attachment files for a specific object record.

        GET /api/{version}/vobjects/{object_name}/{object_record_id}/attachments/file

        Args:
            object_name (str): The object name__v field value
            object_record_id (str): The object record id field value
            directory_path (str): Local directory path where the files will be saved

        Returns:
            dict: Summary of downloaded files

        Notes:
            - The attachments are packaged in a ZIP file with the file name:
              {object type label} {object record name} - attachments.zip
            - The Content-Type header is set to application/zip;charset=UTF-8
            - The Content-Disposition header contains a filename component for naming the local file
        """
        import os

        # Get all attachments for the record
        attachments = self.retrieve_object_record_attachments(
            object_name, object_record_id
        )

        if not os.path.exists(directory_path):
            os.makedirs(directory_path)

        download_summary = {"total": 0, "success": 0, "failed": 0, "files": []}

        if "attachments" in attachments:
            for attachment in attachments["attachments"]:
                try:
                    attachment_id = attachment["id"]
                    filename = attachment.get("filename", f"attachment_{attachment_id}")
                    file_path = os.path.join(directory_path, filename)

                    self.download_object_record_attachment_file(
                        object_name, object_record_id, attachment_id, file_path
                    )

                    download_summary["success"] += 1
                    download_summary["files"].append(
                        {
                            "id": attachment_id,
                            "filename": filename,
                            "path": file_path,
                            "status": "success",
                        }
                    )
                except Exception as e:
                    download_summary["failed"] += 1
                    download_summary["files"].append(
                        {
                            "id": attachment.get("id", "unknown"),
                            "filename": attachment.get("filename", "unknown"),
                            "status": "failed",
                            "error": str(e),
                        }
                    )

                download_summary["total"] += 1

        return download_summary

    def create_object_record_attachment(
        self, object_name, object_record_id, file_path, description=None
    ):
        """
        Creates a new attachment for an object record.

        POST /api/{version}/vobjects/{object_name}/{object_record_id}/attachments

        Args:
            object_name (str): The object name__v field value
            object_record_id (str): The object record id field value
            file_path (str): Path to the file to attach
            description (str, optional): Description for the attachment

        Returns:
            dict: Response from the API with attachment details including id and version

        Notes:
            - If the attachment already exists, Vault uploads it as a new version of the existing attachment
            - Maximum allowed file size is 4GB
            - The following attributes are determined based on the file: filename__v, format__v, size__v
            - If an attachment with the same filename already exists, it's added as a new version
            - If an attachment with the same MD5 checksum exists, the new attachment is not added
        """
        import os

        url = f"api/{self.client.LatestAPIversion}/vobjects/{object_name}/{object_record_id}/attachments"

        files = {"file": (os.path.basename(file_path), open(file_path, "rb"))}

        data = {}
        if description:
            data["description"] = description

        return self.client.api_call(url, method="POST", files=files, data=data)

    def create_multiple_object_record_attachments(
        self, object_name, staged_files_payload
    ):
        """
        Creates multiple object record attachments in bulk via staging.

        POST /api/{version}/vobjects/{object_name}/attachments/batch

        Args:
            object_name (str): The object name__v field value
            staged_files_payload (dict): Payload containing the staged file information including:
                                        - id: The id of the object record
                                        - filename__v: Name for the new attachment with file extension
                                        - file: Filepath of the attachment on file staging
                                        - description__v (optional): Description of the attachment
                                        - external_id__v (optional): External ID value of the attachment

        Returns:
            dict: Response from the API with attachment details

        Notes:
            - Maximum input file size is 1GB
            - Values must be UTF-8 encoded
            - CSVs must follow standard format
            - Maximum batch size is 500
            - If an attachment with the same name already exists, it's added as a new version
            - Maximum allowed file size for attachments is 100 MB
        """
        url = f"api/{self.client.LatestAPIversion}/vobjects/{object_name}/attachments/batch"

        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        data = json.dumps(staged_files_payload)

        return self.client.api_call(url, method="POST", headers=headers, data=data)

    def restore_object_record_attachment_version(
        self, object_name, object_record_id, attachment_id, version_number
    ):
        """
        Restores a previous version of an attachment.

        POST /api/{version}/vobjects/{object_name}/{object_record_id}/attachments/{attachment_id}/versions/{attachment_version}?restore=true

        Args:
            object_name (str): The object name__v field value
            object_record_id (str): The object record id field value
            attachment_id (str): The attachment id field value
            version_number (str): The version number to restore

        Returns:
            dict: Response from the API with restoration details including id and version
        """
        url = f"api/{self.client.LatestAPIversion}/vobjects/{object_name}/{object_record_id}/attachments/{attachment_id}/versions/{version_number}?restore=true"

        return self.client.api_call(url, method="POST")

    def update_object_record_attachment_description(
        self, object_name, object_record_id, attachment_id, description
    ):
        """
        Updates the description of an attachment.

        PUT /api/{version}/vobjects/{object_name}/{object_record_id}/attachments/{attachment_id}

        Args:
            object_name (str): The object name__v field value
            object_record_id (str): The object record id field value
            attachment_id (str): The attachment id field value
            description (str): New description for the attachment

        Returns:
            dict: Response from the API with update details

        Notes:
            - Description is the only editable field for attachments
            - Maximum length for description is 1000 characters
        """
        url = f"api/{self.client.LatestAPIversion}/vobjects/{object_name}/{object_record_id}/attachments/{attachment_id}"

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }

        data = {"description__v": description}

        return self.client.api_call(url, method="PUT", headers=headers, data=data)

    def update_multiple_object_record_attachment_descriptions(
        self, object_name, descriptions_payload
    ):
        """
        Updates descriptions for multiple attachments in bulk.

        PUT /api/{version}/vobjects/{object_name}/attachments/batch

        Args:
            object_name (str): The object name__v field value
            descriptions_payload (dict): Payload containing:
                                        - id: The id of the object record
                                        - attachment_id: The id of the attachment being updated
                                        - description__v: New description for the attachment
                                        - external_id__v (optional): Identify attachments by external id

        Returns:
            dict: Response from the API with update details

        Notes:
            - Maximum input file size is 1GB
            - Values must be UTF-8 encoded
            - CSVs must follow standard format
            - Maximum batch size is 500
            - Can only update the latest version of an attachment
            - To identify attachments by external_id__v, use idParam=external_id__v query parameter
        """
        url = f"api/{self.client.LatestAPIversion}/vobjects/{object_name}/attachments/batch"

        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        data = json.dumps(descriptions_payload)

        return self.client.api_call(url, method="PUT", headers=headers, data=data)

    def delete_object_record_attachment(
        self, object_name, object_record_id, attachment_id
    ):
        """
        Deletes an attachment (latest version and history) from an object record.

        DELETE /api/{version}/vobjects/{object_name}/{object_record_id}/attachments/{attachment_id}

        Args:
            object_name (str): The object name__v field value
            object_record_id (str): The object record id field value
            attachment_id (str): The attachment id field value

        Returns:
            dict: Response from the API with deletion details
        """
        url = f"api/{self.client.LatestAPIversion}/vobjects/{object_name}/{object_record_id}/attachments/{attachment_id}"

        return self.client.api_call(url, method="DELETE")

    def delete_multiple_object_record_attachments(
        self, object_name, attachments_payload
    ):
        """
        Deletes multiple attachments in bulk.

        DELETE /api/{version}/vobjects/{object_name}/attachments/batch

        Args:
            object_name (str): The object name__v field value
            attachments_payload (dict): Payload containing:
                                      - id: The id of the object record
                                      - attachment_id: The id of the attachment being deleted
                                      - external_id__v (optional): Identify attachments by external id

        Returns:
            dict: Response from the API with deletion details

        Notes:
            - Maximum input file size is 1GB
            - Values must be UTF-8 encoded
            - CSVs must follow standard format
            - Maximum batch size is 500
            - To identify attachments by external_id__v, use idParam=external_id__v query parameter
            - Some HTTP clients don't support DELETE requests with a body. As a workaround,
              you can use POST method with _method=DELETE query parameter
        """
        url = f"api/{self.client.LatestAPIversion}/vobjects/{object_name}/attachments/batch"

        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        data = json.dumps(attachments_payload)

        return self.client.api_call(url, method="DELETE", headers=headers, data=data)

    def delete_object_record_attachment_version(
        self, object_name, object_record_id, attachment_id, version_number
    ):
        """
        Deletes a specific version of an attachment from an object record.

        DELETE /api/{version}/vobjects/{object_name}/{object_record_id}/attachments/{attachment_id}/versions/{attachment_version}

        Args:
            object_name (str): The object name__v field value
            object_record_id (str): The object record id field value
            attachment_id (str): The attachment id field value
            version_number (str): The version number to delete

        Returns:
            dict: Response from the API with deletion details
        """
        url = f"api/{self.client.LatestAPIversion}/vobjects/{object_name}/{object_record_id}/attachments/{attachment_id}/versions/{version_number}"

        return self.client.api_call(url, method="DELETE")

    def retrieve_deleted_object_record_attachments(self, object_name, start_date=None, end_date=None, name_filter=None, id_token=None):
        """
        Retrieves all deleted object record attachments.

        GET /api/{version}/objects/deletions/vobjects/{object_name}/attachments

        Args:
            object_name (str): The object name__v field value
            start_date (str, optional): Start date for filtering results (ISO format)
            end_date (str, optional): End date for filtering results (ISO format)
            name_filter (str, optional): Name filter for attachment names
            id_token (str, optional): Security token string for specific deleted attachment

        Returns:
            dict: List of deleted attachments with details including deletion information

        Notes:
            - After object record attachments are deleted, their information is available for retrieval for 30 days
            - Can use optional query parameters to narrow results to specific date/time ranges
            - Dates and times are in UTC
        """
        url = f"api/{self.client.LatestAPIversion}/objects/deletions/vobjects/{object_name}/attachments"

        params = {}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        if name_filter:
            params["name_filter"] = name_filter
        if id_token:
            params["idtoken"] = id_token

        return self.client.api_call(url, params=params)
