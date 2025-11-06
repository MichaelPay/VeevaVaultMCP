from .base_service import BaseDocumentService
import json


class DocumentLocksService(BaseDocumentService):
    """
    Service class for managing document locks in Veeva Vault.

    A document "lock" is analogous to "checking out a document" but without the file attached in the response for download.
    To download the document file after locking it, use the Download Document File endpoint.
    """

    def retrieve_document_lock_metadata(self):
        """
        Retrieves metadata about document locking in the vault.

        Returns metadata fields including name, label, type, scope, required status, and other attributes
        for document lock properties such as locked_by__v and locked_date__v.

        Returns:
            dict: API response containing document lock metadata with properties including:
                - name
                - label
                - type
                - scope
                - required
                - systemAttribute
                - editable
                - setOnCreateOnly
                - objectType (when field type is "ObjectReference")
        """
        url = f"api/{self.client.LatestAPIversion}/metadata/objects/documents/lock"

        return self.client.api_call(url)

    def create_document_lock(self, doc_id):
        """
        Creates a lock on a document to prevent other users from editing it.
        This is analogous to checking out a document but without the file attached in the response for download.

        On success, Vault locks the document and other users are not allowed to lock (check-out) the document.

        Args:
            doc_id (str): ID of the document to lock

        Returns:
            dict: API response indicating success or failure, with a message like "Document successfully checked out."
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/{doc_id}/lock"

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }

        return self.client.api_call(url, method="POST", headers=headers)

    def retrieve_document_lock(self, doc_id):
        """
        Retrieves information about any locks on a specific document.

        If the document is locked (checked out), the response includes the user ID of the person
        who checked it out and the date and time. If the document is not locked, the lock fields
        will not be returned.

        Args:
            doc_id (str): ID of the document to check

        Returns:
            dict: API response containing lock information for the document, including:
                - locked_by__v: The user ID of the person who locked the document
                - locked_date__v: The date and time when the document was locked
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/{doc_id}/lock"

        return self.client.api_call(url)

    def delete_document_lock(self, doc_id):
        """
        Removes a lock from a document (analogous to undoing check out of a document).

        The authenticated user must have Edit Document permission in the document lifecycle state security settings
        as well as one of the following:
        - Document Owner role on the document
        - All Documents: All Document Actions permission
        - Document: Cancel Checkout permission

        On success, Vault unlocks the document, allowing other users to lock/check out the document.

        Args:
            doc_id (str): ID of the document to unlock

        Returns:
            dict: API response indicating success or failure, with a message like "Undo check out successful."
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/{doc_id}/lock"

        return self.client.api_call(url, method="DELETE")

    def undo_collaborative_authoring_checkout(self, doc_ids):
        """
        Undoes collaborative authoring checkout on up to 500 documents at once.

        To undo basic checkout, use delete_document_lock instead.

        On success, Vault returns a responseStatus and responseMessage for each ID in the request.
        Partial success is allowed, meaning some documents in the batch may succeed while others fail.
        For any failed documents, the response includes a reason for the failure.

        Args:
            doc_ids (list): List of document IDs to undo checkout for (maximum 500 documents per request)

        Returns:
            dict: API response with details of the operation status for each document:
                - responseStatus: "SUCCESS", "FAILURE", or "EXCEPTION"
                - responseMessage: Explanation of the result
                - id: The document ID
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/batch/lock"

        headers = {"Content-Type": "text/csv", "Accept": "application/json"}

        # Format document IDs as CSV
        csv_data = "id\n" + "\n".join(str(doc_id) for doc_id in doc_ids)

        # Some HTTP clients don't support DELETE requests with a body, so we use POST with _method=DELETE
        # but our implementation uses DELETE directly as that's what the API requires
        return self.client.api_call(
            url, method="DELETE", headers=headers, data=csv_data
        )

    # These methods appear to be duplicates or alternative names for existing functionality
    # I'm keeping them for backward compatibility, but updating their docstrings to reference
    # the canonical methods

    def lock_document(self, doc_id):
        """
        Locks a document to prevent edits by other users.

        This is an alias for create_document_lock().

        Args:
            doc_id (str): ID of the document to lock

        Returns:
            dict: API response indicating success or failure
        """
        return self.create_document_lock(doc_id)

    def unlock_document(self, doc_id):
        """
        Unlocks a previously locked document.

        This is an alias for delete_document_lock().

        Args:
            doc_id (str): ID of the document to unlock

        Returns:
            dict: API response indicating success or failure
        """
        return self.delete_document_lock(doc_id)

    def create_document_checkout_task(
        self, doc_ids, comments=None, due_date=None, assigned_to_ids=None
    ):
        """
        Creates checkout tasks for multiple documents.

        Note: This endpoint appears to be distinct from the document locks API
        but is related to the document checkout process.

        Args:
            doc_ids (list): List of document IDs to check out
            comments (str, optional): Comments for the checkout
            due_date (str, optional): Due date in ISO format
            assigned_to_ids (list, optional): IDs of users to assign the task to

        Returns:
            dict: API response with details of the created tasks
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/checkout"

        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        data = {"ids": doc_ids}

        if comments:
            data["comments__v"] = comments
        if due_date:
            data["due_date__v"] = due_date
        if assigned_to_ids:
            data["assigned_to_ids"] = assigned_to_ids

        return self.client.api_call(
            url, method="POST", headers=headers, data=json.dumps(data)
        )
