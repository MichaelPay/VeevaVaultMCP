import pandas as pd
from .base_service import BaseObjectService


class ObjectMetadataService(BaseObjectService):
    """
    Service class for handling Veeva Vault object metadata operations.

    Provides methods to retrieve and analyze metadata about objects, fields,
    relationships, and configurations in the Vault.
    """

    def retrieve_object_metadata(self, object_name, loc=False):
        """
        Retrieves detailed metadata for a specific object.

        GET /api/{version}/metadata/vobjects/{object_name}

        Args:
            object_name (str): API name of the object
            loc (bool): Whether to include localized strings for labels and help text

        Returns:
            dict: Object metadata including fields, relationships, and configurations such as
                 allow_attachments, auditable, role_overrides, system_managed, etc.
        """
        url = f"api/{self.client.LatestAPIversion}/metadata/vobjects/{object_name}"

        params = {}
        if loc:
            params["loc"] = "true"

        return self.client.api_call(url, params=params)

    def retrieve_object_field_metadata(self, object_name, object_field_name, loc=False):
        """
        Retrieves detailed metadata for a specific field on an object.

        GET /api/{version}/metadata/vobjects/{object_name}/fields/{object_field_name}

        Args:
            object_name (str): API name of the object
            object_field_name (str): API name of the field
            loc (bool): Whether to include localized strings for labels and help text

        Returns:
            dict: Field metadata including type, required status, editable, facetable, etc.
                 Important metadata includes:
                 - required: When true, field value must be set when creating records
                 - editable: When true, field value can be defined by the user
                 - no_copy: When true, field values are not copied when using Make a Copy
                 - facetable: When true, field is available for faceted filtering
                 - format_mask: The format mask expression if it exists on the field
                 - rollup: When true, this field is a Roll-up field
        """
        url = f"api/{self.client.LatestAPIversion}/metadata/vobjects/{object_name}/fields/{object_field_name}"

        params = {}
        if loc:
            params["loc"] = "true"

        return self.client.api_call(url, params=params)

    def retrieve_object_collection(self, loc=False):
        """
        Retrieves a list of all objects in the vault.

        GET /api/{version}/metadata/vobjects

        Args:
            loc (bool): Whether to include localized strings for labels and help text

        Returns:
            dict: Collection of all objects with summary information including url, label,
                 name, prefix, status, and configuration_state for each object
        """
        url = f"api/{self.client.LatestAPIversion}/metadata/vobjects"

        params = {}
        if loc:
            params["loc"] = "true"

        return self.client.api_call(url, params=params)

    def retrieve_limits_on_objects(self):
        """
        Retrieves information about API limits on objects.

        GET /api/{version}/limits

        Returns:
            dict: Information about API limits including:
                 - records_per_object: Maximum number of records per object
                 - custom_objects: Maximum number of custom objects and number remaining
        """
        url = f"api/{self.client.LatestAPIversion}/limits"

        return self.client.api_call(url)

    def describe_objects(self):
        """
        Retrieves metadata about all available objects in the Vault.

        GET /api/{version}/metadata/vobjects

        Returns:
            pandas.DataFrame: A DataFrame containing object metadata sorted by name
        """
        url = f"api/{self.client.LatestAPIversion}/metadata/vobjects"

        response = self.client.api_call(url)
        objects_data = response.get("objects", [])

        return pd.DataFrame(objects_data).sort_values(by="name")

    def object_field_metadata(self, object_api_name):
        """
        Retrieves metadata about the fields of a specific object.

        GET /api/{version}/metadata/vobjects/{object_name}

        Args:
            object_api_name (str): API name of the object

        Returns:
            pandas.DataFrame: A DataFrame containing field metadata
        """
        url = f"api/{self.client.LatestAPIversion}/metadata/vobjects/{object_api_name}"

        response = self.client.api_call(url)
        fields_data = response.get("object", {}).get("fields", [])

        return pd.DataFrame(fields_data)
