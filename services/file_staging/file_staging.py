import pandas as pd
import asyncio
import requests


class FileStagingService:
    """
    Service class for managing file staging in Veeva Vault.

    This service provides methods to interact with all file staging-related API endpoints,
    allowing listing, downloading, creating, updating, and deleting files and folders,
    as well as managing resumable upload sessions for large files.
    """

    def __init__(self, client):
        """
        Initialize with a VaultClient instance

        Args:
            client: An initialized VaultClient instance for API communication
        """
        self.client = client

    def list_items_at_path(
        self, item_path, recursive=False, limit=1000, format_result=None
    ):
        """
        Return a list of files and folders for the specified path.

        Paths are different for Admin users (Vault Owners and System Admins) and non-Admin users.

        Corresponds to GET /api/{version}/services/file_staging/items/{item}

        Args:
            item_path (str): The absolute path to a file or folder. This path is specific to the
                authenticated user. Admin users can access the root directory. All other users
                can only access their own user directory.
            recursive (bool, optional): If true, the response will contain the contents of
                all subfolders. Default is False.
            limit (int, optional): The maximum number of items per page in the response.
                This can be any value between 1 and 1000. Default is 1000.
            format_result (str, optional): If set to 'csv', the response includes a job_id.
                Use the Job ID value to retrieve the status and results of the request.

        Returns:
            dict: On SUCCESS, the response includes the following information:
                - kind: The kind of item. This can be either file or folder.
                - path: The absolute path, including file or folder name, to the item on file staging.
                - name: The name of the file or folder.
                - size: The size of the file in bytes. Not applicable to folders.
                - modified_date: The timestamp of when the file was last modified. Not applicable to folders.
                - next_page: The pagination URL to navigate to the next page of results.
                - item: The path root for the query. Included in responses where format_result = csv.
        """
        url = f"api/{self.client.LatestAPIversion}/services/file_staging/items/{item_path}"
        params = {"recursive": str(recursive).lower(), "limit": limit}

        if format_result:
            params["format_result"] = format_result

        return self.client.api_call(url, method="GET", params=params)

    def download_item_content(self, item_path, byte_range=None):
        """
        Retrieve the content of a specified file from file staging.

        Use the Range header to create resumable downloads for large files,
        or to continue downloading a file if your session is interrupted.

        Corresponds to GET /api/{version}/services/file_staging/items/content/{item}

        Args:
            item_path (str): The absolute path to a file. This path is specific to the
                authenticated user. Admin users can access the root directory.
                All other users can only access their own user directory.
            byte_range (tuple, optional): A tuple specifying a partial range of bytes to include
                in the download. Maximum 50 MB. Must be in the format (min, max).
                For example, (0, 1000). Default is None which downloads the entire file.

        Returns:
            bytes: On SUCCESS, returns the content of the specified file.
                The HTTP Response Header Content-Type is set to application/octet-stream
                and the HTTP Response Header Content-Disposition contains a filename component.
                If a range header was specified in the request, the response also includes
                the Content-Range HTTP Response Header.
        """
        url = f"api/{self.client.LatestAPIversion}/services/file_staging/items/content/{item_path}"
        headers = {}

        if byte_range:
            headers["Range"] = f"bytes={byte_range[0]}-{byte_range[1]}"

        return self.client.api_call(url, method="GET", headers=headers, return_raw=True)

    def create_folder_or_file(self, path, kind, file=None, overwrite=False):
        """
        Upload files or folders up to 50MB to file staging.

        To upload files larger than 50MB, see resumable upload methods.
        You can only create one file or folder per request.

        Corresponds to POST /api/{version}/services/file_staging/items

        Args:
            path (str): The absolute path, including file or folder name, to place the item
                in file staging. This path is specific to the authenticated user. Admin users
                can access the root directory. All other users can only access their own user directory.
            kind (str): The kind of item to create. This can be either 'file' or 'folder'.
            file (str, optional): For files, the local path to the file to upload.
                Not used for folders. Default is None.
            overwrite (bool, optional): If set to True, Vault will overwrite any existing files
                with the same name at the specified destination. For folders, this is always False.
                Default is False.

        Returns:
            dict: On SUCCESS, the response contains information about the created item:
                For files:
                    - kind: "file"
                    - path: The absolute path to the file
                    - name: The file name
                    - size: The size of the file in bytes
                    - file_content_md5: The MD5 checksum of the file content
                For folders:
                    - kind: "folder"
                    - path: The absolute path to the folder
                    - name: The folder name
        """
        url = f"api/{self.client.LatestAPIversion}/services/file_staging/items"

        data = {
            "path": path,
            "kind": kind,
        }

        if kind == "file" and overwrite:
            data["overwrite"] = "true"

        files = {}
        if kind == "file" and file:
            files = {"file": open(file, "rb")}

        return self.client.api_call(url, method="POST", data=data, files=files)

    def update_folder_or_file(self, item_path, parent=None, name=None):
        """
        Move or rename a folder or file on file staging.

        You can move and rename an item in the same request.

        Corresponds to PUT /api/{version}/services/file_staging/items/{item}

        Args:
            item_path (str): The absolute path to a file or folder. This path is specific
                to the authenticated user. Admin users can access the root directory.
                All other users can only access their own user directory.
            parent (str, optional): When moving a file or folder, specifies the absolute path
                to the parent directory in which to place the file. Default is None.
            name (str, optional): When renaming a file or folder, specifies the new name.
                Default is None.

        Returns:
            dict: On SUCCESS, the response contains the following information:
                - job_id: The Job ID value to retrieve the status and results of the request.
                - url: URL to retrieve the current job status of this request.

        Note:
            At least one of parent or name must be provided.

            Renaming a file in your Vault's Inbox directory creates a new Staged document
            in your Vault and does not rename, remove, or update the previously created
            corresponding Staged document.
        """
        url = f"api/{self.client.LatestAPIversion}/services/file_staging/items/{item_path}"

        data = {}
        if parent:
            data["parent"] = parent
        if name:
            data["name"] = name

        if not data:
            raise ValueError("At least one of 'parent' or 'name' must be provided")

        return self.client.api_call(url, method="PUT", data=data)

    def delete_file_or_folder(self, item_path, recursive=False):
        """
        Delete an individual file or folder from file staging.

        Corresponds to DELETE /api/{version}/services/file_staging/items/{item}

        Args:
            item_path (str): The absolute path to the file or folder to delete. This path
                is specific to the authenticated user. Admin users can access the root directory.
                All other users can only access their own user directory.
            recursive (bool, optional): Applicable to deleting folders only. If true, the request
                will delete the contents of a folder and all subfolders. Default is False.

        Returns:
            dict: On SUCCESS, the response contains the following information:
                - job_id: The Job ID value to retrieve the status and results of the request.
                - url: URL to retrieve the current job status of this request.

        Note:
            Deleting files from your Vault's Inbox directory does not delete corresponding
            Staged documents Vault created when the files were uploaded.
        """
        url = f"api/{self.client.LatestAPIversion}/services/file_staging/items/{item_path}"

        params = {}
        if recursive:
            params["recursive"] = "true"

        return self.client.api_call(url, method="DELETE", params=params)

    def create_resumable_upload_session(self, path, size, overwrite=False):
        """
        Initiate a multipart upload session and return an upload session ID.

        Corresponds to POST /api/{version}/services/file_staging/upload

        Args:
            path (str): The absolute path, including file name, to place the file in the
                staging server. This path is specific to the authenticated user. Admin users
                can access the root directory. All other users can only access their own user directory.
            size (int): The size of the file in bytes. The maximum file size is 500GB.
            overwrite (bool, optional): If set to true, Vault will overwrite any existing files
                with the same name at the specified destination. Default is False.

        Returns:
            dict: Upon SUCCESS, the response includes the following information:
                - path: The path to the file as specified in the request.
                - id: The upload session ID.
                - expiration_date: The timestamp of when the upload session will expire.
                - created_date: The timestamp of when the session was created.
                - last_uploaded_date: The timestamp of the last upload in this session.
                - owner: The user ID of the Vault user who initiated the upload session.
                - uploaded_parts: The number of parts uploaded to the session so far.
                - size: The size of the file in bytes as specified in the request.
                - uploaded: The total size, in bytes, uploaded so far in the session.
        """
        url = f"api/{self.client.LatestAPIversion}/services/file_staging/upload"

        data = {"path": path, "size": size}

        if overwrite:
            data["overwrite"] = "true"

        return self.client.api_call(url, method="POST", data=data)

    def upload_to_session(
        self, upload_session_id, file_part, part_number, content_md5=None
    ):
        """
        Upload parts of a file to an active upload session.

        By default, you can upload up to 2000 parts per upload session, and each part
        can be up to 50MB. Each part must be the same size, except for the last part
        in the upload session.

        Corresponds to PUT /api/{version}/services/file_staging/upload/{upload_session_id}

        Args:
            upload_session_id (str): The upload session ID.
            file_part (bytes or file-like object): The content of the file part to upload.
            part_number (int): The part number, which uniquely identifies a file part and
                defines its position within the file as a whole. If a part is uploaded
                using a part number that has already been used, Vault overwrites the
                previously uploaded file part.
            content_md5 (str, optional): The MD5 checksum of the file part being uploaded.
                Default is None.

        Returns:
            dict: Upon SUCCESS, the response includes the size, part_number, and
                part_content_MD5 for the file part.

        Note:
            Parts must be at least 5MB in size, except for the last part uploaded in a session.
            You must upload parts in numerical order. For example, you cannot upload
            part 3 without first uploading parts 1 and 2.
        """
        url = f"api/{self.client.LatestAPIversion}/services/file_staging/upload/{upload_session_id}"

        headers = {
            "Content-Type": "application/octet-stream",
            "X-VaultAPI-FilePartNumber": str(part_number),
        }

        if content_md5:
            headers["Content-MD5"] = content_md5

        if isinstance(file_part, bytes):
            headers["Content-Length"] = str(len(file_part))

        return self.client.api_call(url, method="PUT", data=file_part, headers=headers)

    def commit_upload_session(self, upload_session_id):
        """
        Mark an upload session as complete and assemble all previously uploaded parts to create a file.

        Corresponds to POST /api/{version}/services/file_staging/upload/{upload_session_id}

        Args:
            upload_session_id (str): The upload session ID.

        Returns:
            dict: On SUCCESS, Vault returns the job_id for the commit.
                Use the Job Status API to retrieve the job results.
                Upon successful completion of the job, the file will be
                available on the staging server.
        """
        url = f"api/{self.client.LatestAPIversion}/services/file_staging/upload/{upload_session_id}"

        headers = {"Content-Type": "application/json"}

        return self.client.api_call(url, method="POST", headers=headers)

    def list_upload_sessions(self):
        """
        Return a list of active upload sessions.

        Corresponds to GET /api/{version}/services/file_staging/upload

        Returns:
            dict: On SUCCESS, Vault lists all active upload sessions for a Vault,
                along with their fields and field values. Admin users will see upload
                sessions for the entire Vault, while non-Admin users will see their own sessions only.

                For each session, the following information is included:
                - path: The absolute path to place the file in the staging server.
                - id: The upload session ID.
                - expiration_date: The timestamp of when the upload session will expire.
                - created_date: The timestamp of when the session was created.
                - last_uploaded_date: The timestamp of the last upload in this session.
                - owner: The user ID of the Vault user who initiated the upload session.
                - uploaded_parts: The number of file parts uploaded so far.
                - size: The total size, in bytes, of the file when complete.
                - uploaded: The total number of bytes uploaded so far in the session.
        """
        url = f"api/{self.client.LatestAPIversion}/services/file_staging/upload"

        return self.client.api_call(url, method="GET")

    def get_upload_session_details(self, upload_session_id):
        """
        Retrieve the details of an active upload session.

        Admin users can get details for all sessions, while non-Admin users can
        only get details for sessions if they are the owner.

        Corresponds to GET /api/{version}/services/file_staging/upload/{upload_session_id}

        Args:
            upload_session_id (str): The upload session ID.

        Returns:
            dict: On SUCCESS, the response includes the following information:
                - path: The absolute path to place the file in the staging server.
                - id: The upload session ID.
                - expiration_date: The timestamp of when the upload session will expire.
                - created_date: The timestamp of when the session was created.
                - last_uploaded_date: The timestamp of the last upload in this session.
                - owner: The user ID of the Vault user who initiated the upload session.
                - uploaded_parts: The total number of file parts uploaded so far.
                - size: The total size, in bytes, of the file when complete.
                - uploaded: The total number of bytes uploaded so far in the session.
        """
        url = f"api/{self.client.LatestAPIversion}/services/file_staging/upload/{upload_session_id}"

        return self.client.api_call(url, method="GET")

    def list_file_parts_uploaded_to_session(self, upload_session_id, limit=1000):
        """
        Return a list of parts uploaded in a session.

        You must be an Admin user or the session owner.

        Corresponds to GET /api/{version}/services/file_staging/upload/{upload_session_id}/parts

        Args:
            upload_session_id (str): The upload session ID.
            limit (int, optional): The maximum number of items per page in the response.
                This can be any value between 1 and 1000. Default is 1000.

        Returns:
            dict: On SUCCESS, the response includes the size and part_number of each
                file part uploaded to the session so far. If the number of parts returned
                exceeds 1000 or the number defined by the limit, Vault includes
                pagination links in the response.
        """
        url = f"api/{self.client.LatestAPIversion}/services/file_staging/upload/{upload_session_id}/parts"

        params = {"limit": limit}

        return self.client.api_call(url, method="GET", params=params)

    def abort_upload_session(self, upload_session_id):
        """
        Abort an active upload session and purge all uploaded file parts.

        Admin users can see and abort all upload sessions, while non-Admin users can
        only see and abort sessions where they are the owner.

        Corresponds to DELETE /api/{version}/services/file_staging/upload/{upload_session_id}

        Args:
            upload_session_id (str): The upload session ID.

        Returns:
            dict: On SUCCESS, returns a response with responseStatus: "SUCCESS".
        """
        url = f"api/{self.client.LatestAPIversion}/services/file_staging/upload/{upload_session_id}"

        return self.client.api_call(url, method="DELETE")
