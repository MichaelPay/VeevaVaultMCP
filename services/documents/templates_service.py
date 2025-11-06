from .base_service import BaseDocumentService
import json


class DocumentTemplatesService(BaseDocumentService):
    """
    Service class for managing document templates in Veeva Vault.

    Document templates allow quick creation of new documents from a configured template.
    When users create a new document from a template, Vault copies the template file and
    uses that copy as the source file for the new document. This bypasses the content upload
    process and allows for more consistent document creation. Document templates are associated
    with a specific document type.
    """

    def get_template_metadata(self):
        """
        Retrieves the metadata which defines the shape of document templates in your Vault.

        Returns:
            dict: Metadata definition for document templates containing field names, types,
                  requiredness, and other attributes.
        """
        url = f"api/{self.client.LatestAPIversion}/metadata/objects/documents/templates"

        headers = {"Accept": "application/json"}

        response = self.client.api_call(url, method="GET", headers=headers)
        return response

    def get_templates(self):
        """
        Retrieves all document templates.

        Returns:
            dict: Collection of document templates configured in the Vault with their attributes.
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/templates"

        headers = {"Accept": "application/json"}

        response = self.client.api_call(url, method="GET", headers=headers)
        return response

    def get_template(self, template_name):
        """
        Retrieves the attributes from a specific document template.

        Args:
            template_name (str): The document template name__v field value.

        Returns:
            dict: Attributes configured on the specified document template.
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/templates/{template_name}"

        headers = {"Accept": "application/json"}

        response = self.client.api_call(url, method="GET", headers=headers)
        return response

    def download_template_file(self, template_name):
        """
        Downloads the file of a specific document template.

        Args:
            template_name (str): The document template name__v field value.

        Returns:
            bytes: The document template file content.
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/templates/{template_name}/file"

        response = self.client.api_call(url, method="GET", raw_response=True)
        return response.content

    def create_template(self, template_data, file_path=None):
        """
        Creates a single document template.

        Note: You cannot create templates if your Vault exceeds template limits.

        Args:
            template_data (dict): Dictionary containing template attributes:
                - name__v (str, optional): The template name. If not included, Vault will generate
                  a value from the label__v.
                - label__v (str, required): The template label visible to users in the UI.
                - type__v (str, required): The document type to associate with the template.
                - subtype__v (str, optional): The document subtype to associate with the template.
                - classification__v (str, optional): The document classification to associate with the template.
                - active__v (bool, required): Whether the template is available for selection.
                - is_controlled__v (bool, optional): Set to true for controlled document templates.
                - template_doc_id__v (str, optional): For controlled templates, the document ID to use as template.
            file_path (str, optional): Path to the template file. Required for basic document templates.
                                      Maximum allowed size is 4GB.

        Returns:
            dict: Response indicating success or failure of the operation.
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/templates"

        headers = {"Accept": "application/json"}

        # If file path is provided, use multipart/form-data
        if file_path:
            headers["Content-Type"] = "multipart/form-data"

            # Prepare form data
            with open(file_path, "rb") as f:
                files = {"file": f}
                response = self.client.api_call(
                    url, method="POST", headers=headers, files=files, data=template_data
                )
        else:
            # For controlled document templates or bulk creation
            headers["Content-Type"] = "application/json"

            response = self.client.api_call(
                url, method="POST", headers=headers, data=json.dumps(template_data)
            )

        return response

    def create_templates_batch(self, templates_data, content_type="application/json"):
        """
        Creates multiple document templates (up to 500).

        Note: You cannot create templates if your Vault exceeds template limits.

        Args:
            templates_data (str or list): Either CSV content as string or list of dictionaries
                                         containing template data.
            content_type (str): Content type of the input data, either "application/json" or "text/csv".

        Returns:
            dict: Response containing success or failure information for each template.
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/templates"

        headers = {"Content-Type": content_type, "Accept": "application/json"}

        if content_type == "application/json":
            data = json.dumps(templates_data)
        else:
            data = templates_data

        response = self.client.api_call(url, method="POST", headers=headers, data=data)

        return response

    def update_template(self, template_name, update_data):
        """
        Updates a single document template.

        Args:
            template_name (str): The document template name__v field value to update.
            update_data (dict): Dictionary containing template attributes to update:
                - new_name (str, optional): New name for the template.
                - label__v (str, optional): New label for the template.
                - active__v (bool, optional): Whether the template is available for selection.
                - template_doc_id__v (str, optional): For converting to controlled templates,
                  the document ID to use as template.

        Returns:
            dict: Response indicating success or failure of the operation.
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/templates/{template_name}"

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }

        response = self.client.api_call(
            url, method="PUT", headers=headers, data=update_data
        )

        return response

    def update_templates_batch(self, templates_data, content_type="application/json"):
        """
        Updates multiple document templates (up to 500).

        Args:
            templates_data (str or list): Either CSV content as string or list of dictionaries
                                         containing template data updates.
            content_type (str): Content type of the input data, either "application/json" or "text/csv".

        Returns:
            dict: Response containing success or failure information for each template update.
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/templates"

        headers = {"Content-Type": content_type, "Accept": "application/json"}

        if content_type == "application/json":
            data = json.dumps(templates_data)
        else:
            data = templates_data

        response = self.client.api_call(url, method="PUT", headers=headers, data=data)

        return response

    def delete_template(self, template_name):
        """
        Deletes a basic document template.

        Note: You cannot delete controlled document templates.

        Args:
            template_name (str): The document template name__v field value to delete.

        Returns:
            dict: Response indicating success or failure of the operation.
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/templates/{template_name}"

        headers = {"Accept": "application/json"}

        response = self.client.api_call(url, method="DELETE", headers=headers)

        return response
