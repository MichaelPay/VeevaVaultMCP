from .base_service import BaseObjectService


class ObjectAttachmentFieldsService(BaseObjectService):
    """
    Service class for handling Veeva Vault object attachment field operations.

    Attachment fields allow you to attach a file to a field on an object record.
    The value of an Attachment field is the file handle for the file.
    """

    def download_attachment_field_file(
        self, object_name, object_record_id, field_name, file_path
    ):
        """
        Downloads the file stored in an attachment field.

        GET /api/{version}/vobjects/{object_name}/{object_record_id}/attachment_fields/{attachment_field_name}/file

        Args:
            object_name (str): API name of the object
            object_record_id (str): ID of the record
            field_name (str): API name of the attachment field
            file_path (str): Local path where the file will be saved

        Returns:
            str: Message indicating successful download

        Notes:
            - The Content-Type header is set to the MIME type of the file
            - If MIME type cannot be detected, Content-Type is set to application/octet-stream
            - The Content-Disposition header contains a filename component for naming the local file
        """
        url = f"api/{self.client.LatestAPIversion}/vobjects/{object_name}/{object_record_id}/attachmentfields/{field_name}/file"

        response = self.client.api_call(url, stream=True, raw_response=True)

        with open(file_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        return "File downloaded successfully"

    def download_all_attachment_field_files(
        self, object_name, object_record_id, directory_path
    ):
        """
        Downloads all files stored in attachment fields for a specific record.

        GET /api/{version}/vobjects/{object_name}/{object_record_id}/attachment_fields/file

        Args:
            object_name (str): API name of the object
            object_record_id (str): ID of the record
            directory_path (str): Local directory path where the files will be saved

        Returns:
            dict: Summary of downloaded files

        Notes:
            - Files are packaged in a ZIP file named: "{object label} {object record name} - attachment fields.zip"
            - When extracted, it includes a subfolder for each Attachment field in the response
            - The Content-Type header is set to application/zip;charset=UTF-8
            - The Content-Disposition header contains a filename component for naming the local file
        """
        import os

        # First, get the record to see available attachment fields
        record = self.client.api_call(
            f"api/{self.client.LatestAPIversion}/vobjects/{object_name}/{object_record_id}"
        )

        if not os.path.exists(directory_path):
            os.makedirs(directory_path)

        download_summary = {"total": 0, "success": 0, "failed": 0, "files": []}

        if "data" in record:
            # Identify attachment fields (fields that end with "__vs")
            attachment_fields = [
                field
                for field in record["data"]
                if field.endswith("__vs") and record["data"][field]
            ]

            for field in attachment_fields:
                try:
                    # Extract filename from field data
                    filename = record["data"][field].get("filename", f"{field}_file")
                    file_path = os.path.join(directory_path, filename)

                    # Download the file
                    self.download_attachment_field_file(
                        object_name, object_record_id, field, file_path
                    )

                    download_summary["success"] += 1
                    download_summary["files"].append(
                        {
                            "field": field,
                            "filename": filename,
                            "path": file_path,
                            "status": "success",
                        }
                    )
                except Exception as e:
                    download_summary["failed"] += 1
                    download_summary["files"].append(
                        {"field": field, "status": "failed", "error": str(e)}
                    )

                download_summary["total"] += 1

        return download_summary

    def update_attachment_field_file(
        self, object_name, object_record_id, field_name, file_path
    ):
        """
        Updates the file stored in an attachment field.

        POST /api/{version}/vobjects/{object_name}/{object_record_id}/attachment_fields/{attachment_field_name}/file

        Args:
            object_name (str): API name of the object
            object_record_id (str): ID of the record
            field_name (str): API name of the attachment field
            file_path (str): Path to the file to upload

        Returns:
            dict: API response with update details

        Notes:
            - If you need to update more than one Attachment field, it's best practice
              to update in bulk with Update Object Records
            - The maximum allowed file size for Attachment fields is 100 MB
        """
        import os

        url = f"api/{self.client.LatestAPIversion}/vobjects/{object_name}/{object_record_id}/attachmentfields/{field_name}"

        with open(file_path, "rb") as f:
            files = {"file": (os.path.basename(file_path), f)}
            return self.client.api_call(url, method="PUT", files=files)
