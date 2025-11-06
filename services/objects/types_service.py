import json
from .base_service import BaseObjectService


class ObjectTypesService(BaseObjectService):
    """
    Service class for handling Veeva Vault object type operations.

    Vault Objects can be partitioned into Object Types. For example, a Product
    object may have different object types like "Pharmaceutical Product" and
    "Medical Device Product" with shared and type-specific fields.
    """

    def retrieve_details_from_all_object_types(self):
        """
        Retrieves details from all object types. Lists all object types and all fields configured on each object type.

        GET /api/{version}/configuration/Objecttype

        Returns:
            dict: Information about all object types and their configured fields
        """
        url = f"api/{self.client.LatestAPIversion}/configuration/Objecttype"

        return self.client.api_call(url)

    def retrieve_details_from_specific_object(self, object_name_and_object_type):
        """
        Retrieves details from a specific object. Lists all object types and all fields configured
        on each object type for the specified object.

        GET /api/{version}/configuration/{object_name_and_object_type}

        Args:
            object_name_and_object_type (str): The object name followed by the object type in the format
                                            Objecttype.{object_name}.{object_type}

        Returns:
            dict: Information about object types and configured fields for the specific object including
                 name, object, active status, description, localized data (if requested), and type_fields
        """
        url = f"api/{self.client.LatestAPIversion}/configuration/{object_name_and_object_type}"

        return self.client.api_call(url)

    def change_object_type(self, object_name, payload):
        """
        Changes the object types assigned to object records. Field values which exist on both the original
        and new object type will carry over to the new type. All other field values will be removed.

        POST /api/{version}/vobjects/{object_name}/actions/changetype

        Args:
            object_name (str): The name of the object
            payload (dict): A dictionary containing at least the "id" and "object_type__v" keys

        Returns:
            dict: Result of the change object type operation

        Notes:
            - Maximum input file size is 1GB
            - Values must be UTF-8 encoded
            - CSVs must follow standard format
            - Maximum batch size is 500
            - Any field values that exist on both original and new object type carry over
            - Field values unique to the original type are removed
            - Required fields:
              - id: The ID of the object record
              - object_type__v: The ID of the new object type
        """
        url = f"api/{self.client.LatestAPIversion}/vobjects/{object_name}/actions/changetype"

        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        data = json.dumps(payload)

        return self.client.api_call(url, method="POST", headers=headers, data=data)
