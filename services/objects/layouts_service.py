from .base_service import BaseObjectService


class ObjectLayoutsService(BaseObjectService):
    """
    Service class for handling Veeva Vault object page layout operations.

    Object page layouts are defined at the object or object-type level and
    control the information displayed to a user on the object record detail page.
    """

    def retrieve_page_layouts(self, object_name):
        """
        Retrieves all page layouts for a specific object.

        GET /api/{version}/metadata/vobjects/{object_name}/page_layouts

        Args:
            object_name (str): API name of the object

        Returns:
            dict: Collection of page layouts for the object including information such as
                 name, label, object_type, active status, description, default_layout status,
                 and display_lifecycle_stages setting

        Notes:
            - Object page layouts are defined at the object or object-type level
            - Objects with multiple object types can define a different layout for each type
        """
        url = f"api/{self.client.LatestAPIversion}/configuration/objects/{object_name}/pagelayouts"

        return self.client.api_call(url)

    def retrieve_page_layout_metadata(self, object_name, layout_name):
        """
        Retrieves detailed metadata for a specific page layout.

        GET /api/{version}/metadata/vobjects/{object_name}/page_layouts/{layout_name}

        Args:
            object_name (str): API name of the object
            layout_name (str): Name of the page layout

        Returns:
            dict: Detailed metadata for the page layout including sections, fields, layout rules,
                 and configuration details

        Notes:
            - The page layout APIs consider the authenticated user's permissions
            - Fields hidden from the user will not be included in the API response
            - Layout rules are not applied, but returned as metadata
            - Both active and inactive fields are included in the response
        """
        url = f"api/{self.client.LatestAPIversion}/configuration/objects/{object_name}/pagelayouts/{layout_name}"

        return self.client.api_call(url)
