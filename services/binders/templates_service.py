import json
from .base_service import BaseBinderService


class BinderTemplatesService(BaseBinderService):
    """
    Service class for managing binder templates in Veeva Vault
    """

    def retrieve_binder_template_metadata(self):
        """
        Retrieves metadata which defines the shape of binder templates.

        The response includes information about all fields available for binder templates,
        including field names, types, requiredness, max length, and other properties.

        Returns:
            dict: API response containing binder template metadata with the following fields:
                - name: The binder template field name (name__v, label__v, type__v, etc.)
                - type: The binder template field type (String, Boolean, Component, or Object)
                - requiredness: Whether a value is required when creating a binder template
                - editable: Whether a value can be added or edited by a user
                - multi_value: Whether the field can have multiple values
                - component: For component fields, defines the data type that can be set
        """
        url = f"api/{self.client.LatestAPIversion}/metadata/objects/binders/templates"

        return self.client.api_call(url)

    def retrieve_binder_template_node_metadata(self):
        """
        Retrieves metadata which defines the shape of binder template nodes.

        Binder "nodes" are individual sections or documents in the binder template hierarchy.
        These can include folders and subfolders in the binder or documents existing within the sections.

        Returns:
            dict: API response containing binder template node metadata with the following fields:
                - name: The binder template node field name
                - type: The binder template field type (ID, String, Number, Enum, or Component)
                - requiredness: Whether a value is required when creating a node
                - editable: Whether a value can be added or edited by a user
                - multi_value: Whether the field can have multiple values
                - component: For component fields, defines the data type that can be set
        """
        url = f"api/{self.client.LatestAPIversion}/metadata/objects/binders/templates/bindernodes"

        return self.client.api_call(url)

    def retrieve_binder_template_collection(self):
        """
        Retrieves the collection of all binder templates.

        The response lists all binder templates which have been added to the Vault,
        including their names, labels, active status, and associated document types.

        Returns:
            dict: API response containing the collection of binder templates including
                 name__v, label__v, active__v, type__v, subtype__v, classification__v,
                 and filing_model__v (for eTMF Vaults) fields.
        """
        url = f"api/{self.client.LatestAPIversion}/objects/binders/templates"

        return self.client.api_call(url)

    def retrieve_binder_template_attributes(self, template_name):
        """
        Retrieves attributes of a specific binder template.

        Args:
            template_name (str): Name of the binder template (name__v field value)

        Returns:
            dict: API response containing template attributes including:
                - name__v: Name of the binder template
                - label__v: Label of the binder template shown to users in the UI
                - active__v: Whether the template is active and available for selection
                - type__v: Vault document type to which the template is associated
                - subtype__v: Vault document subtype (if applicable)
                - classification__v: Vault document classification (if applicable)
                - filing_model__v: eTMF Vaults only - filing model for the template
        """
        url = f"api/{self.client.LatestAPIversion}/objects/binders/templates/{template_name}"

        return self.client.api_call(url)

    def retrieve_binder_template_node_attributes(self, template_name):
        """
        Retrieves attributes of each node (folder/section) of a specific binder template.

        Args:
            template_name (str): Name of the binder template (name__v field value)

        Returns:
            dict: API response containing template node attributes including:
                - id: The binder node (section or planned document) IDs
                - parent_id__v: The node ID of a section or planned document's parent node
                - node_type__v: Binder node types (section or planned_document)
                - label__v: Label of the binder section or planned document
                - number__v: For section nodes, represents the section's hierarchy in the template
                - order__v: Order of the node within the binder or within the parent node
                - type__v: For planned documents, the document type
                - subtype__v: For planned documents, the document subtype (if applicable)
                - classification__v: For planned documents, the document classification (if applicable)
                - lifecycle__v: For planned documents, the associated lifecycle
                - hierarchy_mapping__v: For eTMF Vaults, ID pointing to the TMF reference model
        """
        url = f"api/{self.client.LatestAPIversion}/objects/binders/templates/{template_name}/bindernodes"

        return self.client.api_call(url)

    def create_binder_template(
        self,
        label_v,
        type_v,
        active_v,
        name_v=None,
        subtype_v=None,
        classification_v=None,
    ):
        """
        Creates a new binder template.

        Args:
            label_v (str): Label of the new template. This is what users will see in the UI
                           when selecting a binder template.
            type_v (str): Document type associated with the template.
            active_v (bool): Whether the template should be active (available for selection
                             when creating a binder).
            name_v (str, optional): Name of the template. If not provided, Vault will use
                                   the specified label_v value to generate a name.
            subtype_v (str, optional): Document subtype associated with the template.
                                      Only required if associating the template with a document subtype.
            classification_v (str, optional): Document classification associated with the template.
                                            Only required if associating the template with a document classification.

        Returns:
            dict: API response containing the created template details with name__v field
        """
        url = f"api/{self.client.LatestAPIversion}/objects/binders/templates"

        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        data = {
            "label__v": label_v,
            "type__v": type_v,
            "active__v": str(active_v).lower(),
        }

        if name_v:
            data["name__v"] = name_v
        if subtype_v:
            data["subtype__v"] = subtype_v
        if classification_v:
            data["classification__v"] = classification_v

        return self.client.api_call(
            url, method="POST", headers=headers, data=json.dumps(data)
        )

    def bulk_create_binder_templates(self, csv_data):
        """
        Bulk creates from 1-500 new binder templates.

        The CSV data should include columns for the required fields:
        - name__v (optional): If not included, Vault will generate from label__v
        - label__v (required): Label shown to users in the UI
        - type__v (required): Document type associated with the template
        - subtype__v (optional): Document subtype if applicable
        - classification__v (optional): Document classification if applicable
        - active__v (required): Set to true or false to indicate availability

        Args:
            csv_data (str): CSV data containing template definitions

        Returns:
            dict: API response containing creation results with status for each template
        """
        url = f"api/{self.client.LatestAPIversion}/objects/binders/templates"

        headers = {"Content-Type": "text/csv", "Accept": "application/json"}

        return self.client.api_call(url, method="POST", headers=headers, data=csv_data)

    def create_binder_template_node(self, template_name, csv_data):
        """
        Creates nodes in an existing binder template.

        Binders cannot exceed 50,000 nodes, including component binders. If a binder has
        reached its limit, binder nodes cannot be added to the binder or any of its component
        binders, even if the component binders have not reached the 50,000 node limit.

        The CSV data should include columns for the required fields:
        - id (required): Unique ID for the binder node
        - parent_id__v (required): ID of the parent section (blank for top level)
        - node_type__v (required): Set to 'section' or 'planned_document'
        - label__v (required): Label for the section or planned document
        - order__v (optional): Order of the component within the binder template
        - number__v (optional): For sections, represents hierarchy (e.g., "01", "01.01")
        - type__v, subtype__v, classification__v: Required for planned documents

        Args:
            template_name (str): Name of the template (name__v field value)
            csv_data (str): CSV data containing node definitions

        Returns:
            dict: API response containing node creation results
        """
        url = f"api/{self.client.LatestAPIversion}/objects/binders/templates/{template_name}/bindernodes"

        headers = {"Content-Type": "text/csv", "Accept": "application/json"}

        return self.client.api_call(url, method="POST", headers=headers, data=csv_data)

    def update_binder_template(self, template_name, update_data):
        """
        Updates an existing binder template.

        By changing the document type/subtype/classification, you can move an existing
        binder template to a different level of the document type hierarchy, effectively
        reclassifying the template.

        Fields that can be updated:
        - name__v: Change the name of an existing binder template
        - label__v: Change the label shown in the UI
        - type__v: Change the document type association
        - subtype__v: Change the document subtype association
        - classification__v: Change the document classification association
        - active__v: Enable or disable the template for use

        Args:
            template_name (str): Name of the template to update (name__v field value)
            update_data (dict): Data containing fields to update

        Returns:
            dict: API response containing update results
        """
        url = f"api/{self.client.LatestAPIversion}/objects/binders/templates/{template_name}"

        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        return self.client.api_call(
            url, method="PUT", headers=headers, data=json.dumps(update_data)
        )

    def bulk_update_binder_templates(self, csv_data):
        """
        Bulk updates from 1-500 binder templates.

        The CSV data must include the name__v column to identify which templates to update.
        Other columns that can be included for updates:
        - label__v: Change the label shown in the UI
        - type__v: Change the document type association
        - subtype__v: Change the document subtype association
        - classification__v: Change the document classification association
        - active__v: Enable or disable the template for use

        Including a field name in the CSV but leaving its value blank will clear
        existing values from the field.

        Args:
            csv_data (str): CSV data containing template updates

        Returns:
            dict: API response containing update results
        """
        url = f"api/{self.client.LatestAPIversion}/objects/binders/templates"

        headers = {"Content-Type": "text/csv", "Accept": "application/json"}

        return self.client.api_call(url, method="PUT", headers=headers, data=csv_data)

    def replace_binder_template_nodes(self, template_name, input_data):
        """
        Replaces all binder nodes in an existing binder template.

        This action removes all existing nodes and replaces them with those specified
        in the input. Format requirements for the input data are the same as for
        create_binder_template_node.

        Args:
            template_name (str): Name of the template (name__v field value)
            input_data (str or dict): CSV string or JSON object containing node definitions

        Returns:
            dict: API response containing replacement results
        """
        url = f"api/{self.client.LatestAPIversion}/objects/binders/templates/{template_name}/bindernodes"

        if isinstance(input_data, dict):
            headers = {"Content-Type": "application/json", "Accept": "application/json"}
            data = json.dumps(input_data)
        else:
            headers = {"Content-Type": "text/csv", "Accept": "application/json"}
            data = input_data

        return self.client.api_call(url, method="PUT", headers=headers, data=data)

    def delete_binder_template(self, template_name):
        """
        Deletes an existing binder template.

        Args:
            template_name (str): Name of the template to delete (name__v field value)

        Returns:
            dict: API response indicating success or failure with responseStatus field
        """
        url = f"api/{self.client.LatestAPIversion}/objects/binders/templates/{template_name}"

        return self.client.api_call(url, method="DELETE")
