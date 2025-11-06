import json
import pandas as pd
from .base_service import BaseObjectService


class ObjectCollectionService(BaseObjectService):
    """
    Service class for handling Veeva Vault object collection operations.

    This service provides methods to retrieve collections of object records,
    with support for pagination, sorting, and filtering by specific fields.
    """

    def retrieve_object_record_collection(
        self, object_name, fields=None, limit=None, offset=None, sort=None
    ):
        """
        Retrieves a collection of records for a specific object.

        GET /api/{version}/vobjects/{object_name}

        Args:
            object_name (str): API name of the object
            fields (list): List of field names to include in the response
            limit (int): Maximum number of records to return (max 200)
            offset (int): Starting position for record retrieval (for pagination)
            sort (str): Field name to sort by with optional direction (e.g., "name__v:desc")

        Returns:
            dict: Collection of object records with metadata and data sections
                 The response includes the object metadata and the id and name__v of all records
                 By default, Vault returns a maximum of 200 records per page

        Notes:
            - By default, Vault returns a maximum of 200 object records per page
            - The sort operator can be used for descending (desc) or ascending (asc) order
            - For pagination, you can use the offset operator or next_page/previous_page URLs
            - The pagination URLs remain active for about 15 minutes following the query
        """
        url = f"api/{self.client.LatestAPIversion}/vobjects/{object_name}"

        params = {}
        if fields:
            params["fields"] = ",".join(fields) if isinstance(fields, list) else fields
        if limit:
            params["limit"] = limit
        if offset:
            params["offset"] = offset
        if sort:
            params["sort"] = sort

        return self.client.api_call(url, params=params)

    def retrieve_object_record_collection_as_dataframe(
        self, object_name, fields=None, limit=None, offset=None, sort=None
    ):
        """
        Retrieves a collection of records for a specific object and returns as a pandas DataFrame.

        Args:
            object_name (str): API name of the object
            fields (list): List of field names to include in the response
            limit (int): Maximum number of records to return (max 200)
            offset (int): Starting position for record retrieval (for pagination)
            sort (str): Field name to sort by with optional direction (e.g., "name__v:desc")

        Returns:
            pandas.DataFrame: DataFrame containing the object records
        """
        response = self.retrieve_object_record_collection(
            object_name, fields, limit, offset, sort
        )

        if "data" in response:
            return pd.DataFrame(response.get("data", []))
        return pd.DataFrame()
