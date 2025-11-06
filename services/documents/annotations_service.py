import os
import json
from .base_service import BaseDocumentService


class DocumentAnnotationsService(BaseDocumentService):
    """
    Service class for managing document annotations in Veeva Vault.

    This service provides methods to interact with Veeva Vault's annotation functionality,
    including retrieving, creating, updating, and deleting annotations across documents.
    """

    def retrieve_annotation_type_metadata(self, annotation_type):
        """
        Retrieves the metadata of an annotation type, including metadata and value sets
        for all supported fields on the annotation type.

        Args:
            annotation_type (str): The name of the annotation type. Valid annotation types include:
                note__sys, line__sys, document_link__sys, permalink_link__sys, anchor__sys,
                reply__sys, external_link__sys, suggested_link__sys, approved_link__sys,
                auto_link__sys, keyword_link__sys.

        Returns:
            dict: API response containing metadata information for the specified annotation type.
        """
        url = f"api/{self.client.LatestAPIversion}/metadata/objects/documents/annotations/types/{annotation_type}"

        return self.client.api_call(url)

    def retrieve_annotation_placemark_type_metadata(self, placemark_type):
        """
        Retrieves the metadata of a specified annotation placemark type.

        Args:
            placemark_type (str): The name of the placemark type (e.g., sticky__sys).

        Returns:
            dict: API response containing metadata information for the specified placemark type.
        """
        url = f"api/{self.client.LatestAPIversion}/metadata/objects/documents/annotations/placemarks/types/{placemark_type}"

        return self.client.api_call(url)

    def retrieve_annotation_reference_type_metadata(self, reference_type):
        """
        Retrieves the metadata of a specified annotation reference type.

        Args:
            reference_type (str): The name of the reference type (e.g., permalink__sys).

        Returns:
            dict: API response containing metadata information for the specified reference type.
        """
        url = f"api/{self.client.LatestAPIversion}/metadata/objects/documents/annotations/references/types/{reference_type}"

        return self.client.api_call(url)

    def create_multiple_annotations(self, annotation_data_list):
        """
        Creates up to 500 annotations in a batch operation.

        Args:
            annotation_data_list (list): List of annotation objects, each containing annotation properties.
                Each annotation must include fields like type__sys, document_version_id__sys, and placemark.

        Returns:
            dict: API response with details of the created annotations.
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/annotations/batch"

        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        return self.client.api_call(
            url, method="POST", headers=headers, data=json.dumps(annotation_data_list)
        )

    def add_annotation_replies(self, reply_data_list):
        """
        Creates up to 500 annotation replies in a batch operation.

        Args:
            reply_data_list (list): List of reply objects. Each object must contain
                document_version_id__sys, type__sys (as 'reply__sys'), comment__sys,
                and a placemark object with type__sys ('reply__sys') and reply_parent__sys.

        Returns:
            dict: API response with details of the created replies.
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/annotations/replies/batch"

        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        return self.client.api_call(
            url, method="POST", headers=headers, data=json.dumps(reply_data_list)
        )

    def update_annotations(self, annotation_data_list):
        """
        Updates up to 500 existing annotations in a batch operation.

        Args:
            annotation_data_list (list): List of annotation objects. Each object must contain
                id__sys, document_version_id__sys, and the fields to be updated.

        Returns:
            dict: API response with details of the updated annotations.
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/annotations/batch"

        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        return self.client.api_call(
            url, method="PUT", headers=headers, data=json.dumps(annotation_data_list)
        )

    def read_annotations_by_document_version_and_type(
        self,
        doc_id,
        major_version,
        minor_version,
        annotation_types=None,
        offset=None,
        limit=None,
        pagination_id=None,
    ):
        """
        Retrieves annotations from a specific document version. You can retrieve all annotations
        or choose to retrieve only certain annotation types.

        Args:
            doc_id (str): The document id field value.
            major_version (str): The document major version number.
            minor_version (str): The document minor version number.
            annotation_types (str, optional): The type(s) of annotations to retrieve as comma-separated values
                (e.g., "note__sys,anchor__sys"). If omitted, all annotation types except replies are returned.
            offset (int, optional): The amount of offset from the first record returned for pagination.
            limit (int, optional): Maximum number of records per page (1-500, default 500).
            pagination_id (str, optional): A unique identifier used for paginated results.

        Returns:
            dict: API response with details of document annotations.
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/{doc_id}/versions/{major_version}/{minor_version}/annotations"

        params = {}
        if annotation_types:
            params["annotation_types"] = annotation_types
        if offset is not None:
            params["offset"] = offset
        if limit is not None:
            params["limit"] = limit
        if pagination_id:
            params["pagination_id"] = pagination_id

        return self.client.api_call(url, params=params)

    def read_annotations_by_id(
        self, doc_id, major_version, minor_version, annotation_id
    ):
        """
        Retrieves a specific annotation by the annotation ID.

        Args:
            doc_id (str): The document id field value.
            major_version (str): The document major version number.
            minor_version (str): The document minor version number.
            annotation_id (str): The annotation ID.

        Returns:
            dict: API response with details of the specific annotation.
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/{doc_id}/versions/{major_version}/{minor_version}/annotations/{annotation_id}"

        return self.client.api_call(url)

    def read_replies_of_parent_annotation(
        self, doc_id, major_version, minor_version, annotation_id
    ):
        """
        Retrieves all replies to a specific parent annotation.

        Args:
            doc_id (str): The document id field value.
            major_version (str): The document major version number.
            minor_version (str): The document minor version number.
            annotation_id (str): The parent annotation ID.

        Returns:
            dict: API response with details of all replies to the specified annotation.
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/{doc_id}/versions/{major_version}/{minor_version}/annotations/{annotation_id}/replies"

        return self.client.api_call(url)

    def delete_annotations(self, annotation_data_list):
        """
        Deletes up to 500 annotations in a batch operation.

        Args:
            annotation_data_list (list): List of annotation objects. Each object must contain
                id__sys and document_version_id__sys.

        Returns:
            dict: API response with details of the deleted annotations.
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/annotations/batch"

        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        return self.client.api_call(
            url, method="DELETE", headers=headers, data=json.dumps(annotation_data_list)
        )

    def export_document_annotations_to_pdf(self, doc_id):
        """
        Exports the latest version of a document, along with its annotations, as an annotated PDF.
        This is equivalent to the Export Annotations action in the Vault document viewer UI.

        Args:
            doc_id (str): The document id field value.

        Returns:
            bytes: The PDF data containing the document with annotations.
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/{doc_id}/annotations/file"

        headers = {"Accept": "*/*"}

        response = self.client.api_call(url, headers=headers, raw_response=True)
        return response.content

    def export_document_version_annotations_to_pdf(
        self, doc_id, major_version, minor_version
    ):
        """
        Exports a specific version of a document, along with its annotations, as an annotated PDF.
        This is equivalent to the Export Annotations action in the Vault document viewer UI.

        Args:
            doc_id (str): The document id field value.
            major_version (str): The document major version number.
            minor_version (str): The document minor version number.

        Returns:
            bytes: The PDF data containing the document version with annotations.
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/{doc_id}/versions/{major_version}/{minor_version}/annotations/file"

        headers = {"Accept": "*/*"}

        response = self.client.api_call(url, headers=headers, raw_response=True)
        return response.content

    def import_document_annotations_from_pdf(self, doc_id, file_path):
        """
        Uploads document annotations from a PDF file. The file must be a PDF created by exporting
        annotations for the latest version of the same document.

        Args:
            doc_id (str): The document id field value.
            file_path (str): The path to the document file that contains the annotations to be uploaded.

        Returns:
            dict: A dictionary containing details about the upload status including the number
                 of replies, failures, and new annotations.
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/{doc_id}/annotations/file"

        with open(file_path, "rb") as file:
            files = {"file": (os.path.basename(file_path), file)}
            return self.client.api_call(url, method="POST", files=files)

    def import_document_version_annotations_from_pdf(
        self, doc_id, major_version, minor_version, file_path
    ):
        """
        Uploads annotations for a specific document version from a PDF file. The file must be a PDF
        created by exporting annotations for the specified version of the same document.

        Args:
            doc_id (str): The document id field value.
            major_version (str): The document major version number.
            minor_version (str): The document minor version number.
            file_path (str): The path to the document file that contains the annotations to be uploaded.

        Returns:
            dict: A dictionary containing details about the upload status.
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/{doc_id}/versions/{major_version}/{minor_version}/annotations/file"

        with open(file_path, "rb") as file:
            files = {"file": (os.path.basename(file_path), file)}
            return self.client.api_call(url, method="POST", files=files)

    def retrieve_video_annotations(self, doc_id, major_version, minor_version):
        """
        Retrieves annotations on a video document.

        Args:
            doc_id (str): The video document id field value.
            major_version (str): The video document major version number.
            minor_version (str): The video document minor version number.

        Returns:
            str: A CSV containing the video annotation metadata including replies and ordered by time signature.
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/{doc_id}/versions/{major_version}/{minor_version}/export-video-annotations"

        headers = {"Accept": "text/csv"}

        response = self.client.api_call(url, headers=headers, raw_response=True)
        return response.text

    def retrieve_document_anchors(self, doc_id):
        """
        Retrieves all anchor IDs from the latest version of a document.

        Args:
            doc_id (str): The document id field value.

        Returns:
            dict: API response with details of document anchors including anchor ID,
                 note ID, anchor name, author, timestamp, and page number.
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/{doc_id}/anchors"

        return self.client.api_call(url)

    def retrieve_document_version_notes_as_csv(
        self, doc_id, major_version, minor_version
    ):
        """
        Retrieves notes in CSV format for any document that has a viewable rendition and at least one annotation.

        Args:
            doc_id (str): The document id field value.
            major_version (str): The document major version number.
            minor_version (str): The document minor version number.

        Returns:
            str: A CSV containing the annotation metadata.
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/{doc_id}/versions/{major_version}/{minor_version}/doc-export-annotations-to-csv"

        headers = {"Accept": "text/csv"}

        response = self.client.api_call(url, headers=headers, raw_response=True)
        return response.text

    def create_document_annotation(
        self, doc_id, annotation_data, major_version=None, minor_version=None
    ):
        """
        Creates an annotation on a document or a specific document version.
        Note: For batch creation of multiple annotations, use create_multiple_annotations.

        Args:
            doc_id (str): ID of the document
            annotation_data (dict): Annotation details
            major_version (int, optional): Major version number
            minor_version (int, optional): Minor version number

        Returns:
            dict: API response with details of the created annotation
        """
        # Determine URL based on whether we're creating an annotation for a specific version
        if major_version is not None and minor_version is not None:
            url = f"api/{self.client.LatestAPIversion}/objects/documents/{doc_id}/versions/{major_version}/{minor_version}/annotations"
        else:
            url = f"api/{self.client.LatestAPIversion}/objects/documents/{doc_id}/annotations"

        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        return self.client.api_call(
            url, method="POST", headers=headers, data=json.dumps(annotation_data)
        )

    def retrieve_document_annotations(
        self, doc_id, major_version=None, minor_version=None
    ):
        """
        Retrieves annotations for a document or document version.

        Args:
            doc_id (str): ID of the document
            major_version (int, optional): Major version number
            minor_version (int, optional): Minor version number

        Returns:
            dict: API response with details of document annotations
        """
        # Determine URL based on whether we're retrieving annotations for a specific version
        if major_version is not None and minor_version is not None:
            url = f"api/{self.client.LatestAPIversion}/objects/documents/{doc_id}/versions/{major_version}/{minor_version}/annotations"
        else:
            url = f"api/{self.client.LatestAPIversion}/objects/documents/{doc_id}/annotations"

        return self.client.api_call(url)

    def download_document_annotations(self, doc_id):
        """
        Downloads the annotations of the latest version of a document as a PDF.
        Equivalent to export_document_annotations_to_pdf.

        Args:
            doc_id (str): The ID of the document whose annotations need to be downloaded.

        Returns:
            bytes: The PDF data containing the annotations.
        """
        url = (
            f"api/{self.client.LatestAPIversion}/objects/documents/{doc_id}/annotations"
        )

        headers = {"Accept": "*/*"}

        response = self.client.api_call(url, headers=headers, raw_response=True)
        return response.content

    def download_document_version_annotations(
        self, doc_id, major_version, minor_version
    ):
        """
        Downloads the annotations of the specified document version as a PDF.
        Equivalent to export_document_version_annotations_to_pdf.

        Args:
            doc_id (str): The ID of the document.
            major_version (str): The major version number of the document.
            minor_version (str): The minor version number of the document.

        Returns:
            bytes: The PDF data containing the annotations.
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/{doc_id}/versions/{major_version}/{minor_version}/annotations"

        headers = {"Accept": "*/*"}

        response = self.client.api_call(url, headers=headers, raw_response=True)
        return response.content
