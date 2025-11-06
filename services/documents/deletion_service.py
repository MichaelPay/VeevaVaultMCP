import json
from typing import Dict, Any, Optional, Union, List
from .base_service import BaseDocumentService


class DocumentDeletionService(BaseDocumentService):
    """
    Service class for deleting documents and document versions in Veeva Vault.

    After deleting documents, the API allows you to retrieve their IDs for up to 30 days.
    The deleted files themselves are removed from the server and can only be retrieved by Vault Support.
    Note that you cannot delete checked out documents unless you have the Power Delete permission.
    """

    def delete_single_document(self, document_id: Union[str, int]) -> Dict[str, Any]:
        """
        Deletes all versions of a document, including all source files and viewable renditions.

        If you need to delete more than one document, it is best practice to use the bulk API.

        Args:
            document_id (Union[str, int]): The system-assigned document ID of the document to delete.

        Returns:
            Dict[str, Any]: API response containing details of the deleted document.
                Example: {
                    "responseStatus": "SUCCESS",
                    "id": 534
                }
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/{document_id}"

        headers = {"Accept": "application/json"}

        return self.client.api_call(url, method="DELETE", headers=headers)

    def delete_multiple_documents(
        self, csv_data: Union[str, bytes], id_param: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Deletes all versions of multiple documents, including all source files and viewable renditions.

        The maximum input file size is 1GB.
        The values in the input must be UTF-8 encoded.
        CSVs must follow the standard RFC 4180 format, with some exceptions.
        The maximum batch size is 500.

        Some HTTP clients do not support DELETE requests with a body. As a workaround for these cases,
        you can simulate this request using the POST method with the _method=DELETE query parameter.

        Args:
            csv_data (Union[str, bytes]): CSV content containing document IDs to delete.
                The CSV should include columns for document identification:
                - id: The system-assigned document ID of the document to delete.
                  Not required if providing a unique field identifier (idParam) such as external_id__v.
                - external_id__v: Instead of id, you can use this user-defined document external ID.

            id_param (str, optional): If you're identifying documents in your input by a unique field,
                                    specify the field name (e.g., "external_id__v").
                                    You can use any object field which has unique set to true in the
                                    object metadata, with the exception of picklists.

        Returns:
            Dict[str, Any]: API response containing details of the deleted documents.
                Example: {
                    "responseStatus": "SUCCESS",
                    "data": [
                        {
                            "responseStatus": "SUCCESS",
                            "id": 771,
                            "external_id__v": "ALT-DOC-0771"
                        },
                        {
                            "responseStatus": "SUCCESS",
                            "id": 772,
                            "external_id__v": "CHO-DOC-0772"
                        },
                        {
                            "responseStatus": "FAILURE",
                            "errors": [
                                {
                                    "type": "INVALID_DATA",
                                    "message": "Error message describing why this document was not deleted."
                                }
                            ]
                        }
                    ]
                }
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/batch"

        headers = {"Content-Type": "text/csv", "Accept": "application/json"}

        params = {}
        if id_param:
            params["idParam"] = id_param

        # Ensure csv_data is bytes
        if isinstance(csv_data, str):
            csv_data = csv_data.encode("utf-8")

        return self.client.api_call(
            url, method="DELETE", headers=headers, params=params, data=csv_data
        )

    def delete_single_document_version(
        self,
        doc_id: Union[str, int],
        major_version: Union[str, int],
        minor_version: Union[str, int],
    ) -> Dict[str, Any]:
        """
        Deletes a specific version of a document, including the version's source file and viewable rendition.
        Other versions of the document remain unchanged.

        If you need to delete more than one document version, it is best practice to use the bulk API.

        Args:
            doc_id (Union[str, int]): The document id field value.
            major_version (Union[str, int]): The document major_version_number__v field value.
            minor_version (Union[str, int]): The document minor_version_number__v field value.

        Returns:
            Dict[str, Any]: API response containing details of the deleted document version.
                Example: {
                    "responseStatus": "SUCCESS",
                    "id": 534
                }
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/{doc_id}/versions/{major_version}/{minor_version}"

        headers = {"Accept": "application/json"}

        return self.client.api_call(url, method="DELETE", headers=headers)

    def delete_multiple_document_versions(
        self, csv_data: Union[str, bytes], id_param: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Deletes a specific version of multiple documents, including the version's source file and viewable rendition.

        The maximum input file size is 1GB.
        The values in the input must be UTF-8 encoded.
        CSVs must follow the standard RFC 4180 format, with some exceptions.
        The maximum batch size is 500.

        Some HTTP clients do not support DELETE requests with a body. As a workaround for these cases,
        you can simulate this request using the POST method with the _method=DELETE query parameter.

        Args:
            csv_data (Union[str, bytes]): CSV content containing document version details.
                The CSV should include columns for document identification:
                - id: The system-assigned document ID of the document to delete.
                  Not required if providing a unique field identifier (idParam) such as external_id__v.
                - external_id__v: Instead of id, you can use this user-defined document external ID.
                - major_version_number__v: Major version number of the document version to remove.
                - minor_version_number__v: Minor version number of the document version to remove.

            id_param (str, optional): If you're identifying documents in your input by a unique field,
                                    specify the field name (e.g., "external_id__v").
                                    You can use any object field which has unique set to true in the
                                    object metadata, with the exception of picklists.

        Returns:
            Dict[str, Any]: API response containing details of the deleted document versions.
                Example: {
                    "responseStatus": "SUCCESS",
                    "data": [
                        {
                            "responseStatus": "SUCCESS",
                            "id": 771,
                            "external_id__v": "ALT-DOC-0771",
                            "major_version_number__v": 0,
                            "minor_version_number__v": 2
                        },
                        {
                            "responseStatus": "FAILURE",
                            "errors": [
                                {
                                    "type": "INVALID_DATA",
                                    "message": "Error message describing why this document version was not deleted."
                                }
                            ]
                        }
                    ]
                }
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/versions/batch"

        headers = {"Content-Type": "text/csv", "Accept": "application/json"}

        params = {}
        if id_param:
            params["idParam"] = id_param

        # Ensure csv_data is bytes
        if isinstance(csv_data, str):
            csv_data = csv_data.encode("utf-8")

        return self.client.api_call(
            url, method="DELETE", headers=headers, params=params, data=csv_data
        )

    def retrieve_deleted_document_ids(
        self, start_date: Optional[str] = None, end_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Retrieves IDs of documents deleted within the past 30 days.

        After documents and document versions are deleted, their IDs remain available for retrieval for 30 days.
        After that, they cannot be retrieved. This request supports optional parameters to narrow the results
        to a specific date and time range within the past 30 days.

        To completely restore a document deleted within the last 30 days, contact Veeva support.

        Args:
            start_date (str, optional): Specify a date (no more than 30 days past) after which Vault will look for
                                      deleted documents. Dates must be in YYYY-MM-DDTHH:MM:SSZ format.
                                      Example: 2016-01-15T07:00:00Z for 7AM on January 15, 2016.

            end_date (str, optional): Specify a date (no more than 30 days past) before which Vault will look for
                                    deleted documents. Dates must be in YYYY-MM-DDTHH:MM:SSZ format.
                                    Example: 2016-01-15T07:00:00Z for 7AM on January 15, 2016.

        Returns:
            Dict[str, Any]: API response containing details of deleted documents.
                Response includes the following details:
                - total: The total number of deleted documents and document versions.
                - id: The ID of the deleted document or version. If the same document has multiple deleted versions,
                     the same ID may appear twice.
                - major_version_number__v: The major version of the deleted version. If all versions of the document
                                         were deleted, this value is blank ("").
                - minor_version_number__v: The minor version of the deleted version. If all versions of the document
                                         were deleted, this value is blank ("").
                - date_deleted: The date and time this document or version was deleted.
                - global_id__sys: The global ID of the deleted document or version.
                - global_version_id__sys: The global version ID of the deleted document or version. If all versions
                                        of the document were deleted, this value is null.
                - external_id__v: The external ID of the deleted document or version. May be null if no external ID
                                was set for this document.
                - deletion_type: Describes how this document or version was deleted:
                                - document__sys: This document was deleted in full, including all versions.
                                - document_version__sys: This document version was deleted.
                                - version_change__sys: This document version no longer exists, as it became a new
                                                     major version through the Set new major version entry action.

                Example: {
                    "responseStatus": "SUCCESS",
                    "responseMessage": "OK",
                    "responseDetails": {
                        "total": 3,
                        "size": 3,
                        "limit": 1000,
                        "offset": 0
                    },
                    "data": [
                        {
                            "id": 23,
                            "major_version_number__v": 0,
                            "minor_version_number__v": 1,
                            "date_deleted": "2021-02-26T23:46:49Z",
                            "global_id__sys": "10000760_23",
                            "global_version_id__sys": "10000760_23_39",
                            "external_id__v": null,
                            "deletion_type": "version_change__sys"
                        },
                        {
                            "id": 10,
                            "major_version_number__v": "",
                            "minor_version_number__v": "",
                            "date_deleted": "2021-02-26T23:55:45Z",
                            "global_id__sys": "10000760_10",
                            "global_version_id__sys": null,
                            "external_id__v": null,
                            "deletion_type": "document__sys"
                        }
                    ]
                }
        """
        url = f"api/{self.client.LatestAPIversion}/objects/deletions/documents"

        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        params = {}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date

        return self.client.api_call(url, method="GET", headers=headers, params=params)
