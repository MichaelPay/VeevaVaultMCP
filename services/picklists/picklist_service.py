import pandas as pd
import asyncio
import requests


class PicklistService:
    """
    Service class for managing picklists in Veeva Vault.

    This service provides methods to interact with all picklist-related API endpoints,
    allowing retrieval, creation, updating, and inactivation of picklist values.
    """

    def __init__(self, client):
        """
        Initialize with a VaultClient instance

        Args:
            client: An initialized VaultClient instance for API communication
        """
        self.client = client

    def retrieve_all_picklists(self):
        """
        Retrieves all picklists in the Vault.

        Corresponds to GET /api/{version}/objects/picklists

        Returns:
            dict: The JSON response containing all picklists with the following fields:
                - name: Picklist name used in API and displayed in Admin UI
                - label: Picklist label visible to users
                - kind: Type of picklist (global or user)
                - systemManaged: If true, picklist values cannot be modified
                - usedIn: Document types or objects where the picklist is defined
                  (includes objectName, documentTypeName, and propertyName as applicable)
        """
        url = f"api/{self.client.LatestAPIversion}/objects/picklists"
        return self.client.api_call(url)

    def retrieve_picklist_values(self, picklist_name):
        """
        Retrieves all values of a specified picklist.

        Corresponds to GET /api/{version}/objects/picklists/{picklist_name}

        On SUCCESS, returns all available values configured on a picklist in ascending order,
        designated by the picklist value's order attribute. For system-managed picklists with
        dependencies, also returns the controllingPicklistName and picklistDependencies.

        Args:
            picklist_name (str): The API name of the picklist

        Returns:
            pandas.DataFrame: DataFrame containing the picklist values with columns:
                - name: The picklist value name used in API
                - label: The picklist value label displayed to users
                - picklistName: The name of the parent picklist

        Raises:
            Exception: If the API request fails
        """
        url = f"api/{self.client.LatestAPIversion}/objects/picklists/{picklist_name}"
        response = self.client.api_call(url)

        if response["responseStatus"] == "SUCCESS":
            # Check if response uses "picklistValues" (from documentation)
            # or "values" (from current implementation)
            values = response.get("picklistValues", response.get("values", []))
            if values:
                df = pd.DataFrame(values)
                df["picklistName"] = picklist_name
                return df
            else:
                return pd.DataFrame(
                    columns=["name", "label", "status", "id", "picklistName"]
                )
        else:
            raise Exception(f"Failed to retrieve picklist values: {response}")

    def create_picklist_values(self, picklist_name, values):
        """
        Creates new values in the specified picklist.

        Corresponds to POST /api/{version}/objects/picklists/{picklist_name}

        You can add up to 2,000 values to any picklist. The API uses the provided labels
        to create appropriate picklist value names automatically.

        Args:
            picklist_name (str): The API name of the picklist
            values (list): List of picklist value labels to create
                Example: ["North America", "Central America", "South America"]

        Returns:
            dict: The API response containing information about created values:
                - responseStatus: "SUCCESS" if successful
                - responseMessage: A message indicating the operation result
                - picklistValues: List of created values with their names and labels
        """
        url = f"api/{self.client.LatestAPIversion}/objects/picklists/{picklist_name}"

        # Format as form data with value_1, value_2, etc. as required by the API
        data = {}
        for i, value in enumerate(values, 1):
            data[f"value_{i}"] = value

        return self.client.api_call(url, method="POST", data=data)

    def update_picklist_value_label(self, picklist_name, label_updates):
        """
        Updates the labels of existing picklist values.

        Corresponds to PUT /api/{version}/objects/picklists/{picklist_name}

        Changes only the label of picklist values while keeping the names unchanged.
        Use caution when editing picklist labels as they affect all existing document
        and object metadata that refer to the picklist.

        Args:
            picklist_name (str): The API name of the picklist
            label_updates (dict): Dictionary mapping picklist value names to new labels
                Example: {"north_america__c": "North America/United States"}

        Returns:
            dict: The API response containing information about updated values:
                - responseStatus: "SUCCESS" if successful
                - responseMessage: A message indicating the operation result
                - picklistValues: List of updated values with their names and new labels
        """
        url = f"api/{self.client.LatestAPIversion}/objects/picklists/{picklist_name}"

        # The API expects form data where each parameter is a picklist value name
        # and its value is the new label

        return self.client.api_call(url, method="PUT", data=label_updates)

    def update_picklist_value(
        self, picklist_name, picklist_value_name, new_name=None, status=None
    ):
        """
        Updates a picklist value's name or status.

        Corresponds to PUT /api/{version}/objects/picklists/{picklist_name}/{picklist_value_name}

        Use caution when editing picklist value names as they may affect existing document
        and object metadata that refer to the picklist, and can break existing integrations
        that access picklist values via the API.

        Args:
            picklist_name (str): The API name of the picklist
            picklist_value_name (str): The current name of the picklist value
            new_name (str, optional): The new name for the picklist value. Vault adds __c after
                                     processing. Special characters and double underscores __
                                     are not allowed. Defaults to None.
            status (str, optional): The new status for the picklist value. Valid values are
                                   'active' or 'inactive'. Defaults to None.

        Returns:
            dict: The API response indicating success or failure

        Note:
            At least one of new_name or status must be provided.
        """
        url = f"api/{self.client.LatestAPIversion}/objects/picklists/{picklist_name}/{picklist_value_name}"

        data = {}
        if new_name:
            data["name"] = new_name
        if status:
            data["status"] = status

        return self.client.api_call(url, method="PUT", data=data)

    def inactivate_picklist_value(self, picklist_name, picklist_value_name):
        """
        Inactivates a value from a picklist.

        Corresponds to DELETE /api/{version}/objects/picklists/{picklist_name}/{picklist_value_name}

        This does not affect picklist values that are already in use.

        Args:
            picklist_name (str): The API name of the picklist
            picklist_value_name (str): The name of the picklist value to inactivate

        Returns:
            dict: The API response containing:
                - responseStatus: "SUCCESS" if successful
                - responseMessage: A message indicating the operation result
                - name: The name of the inactivated picklist value
        """
        url = f"api/{self.client.LatestAPIversion}/objects/picklists/{picklist_name}/{picklist_value_name}"

        return self.client.api_call(url, method="DELETE")

    async def async_bulk_retrieve_picklist_values(self, picklist_names):
        """
        Retrieves values from multiple picklists in parallel.

        This is a helper method that makes multiple calls to retrieve_picklist_values()
        asynchronously for improved performance when working with multiple picklists.

        Args:
            picklist_names (list): List of picklist API names

        Returns:
            pandas.DataFrame: DataFrame containing the combined picklist values
        """
        tasks = []

        # Create tasks for each picklist
        for picklist_name in picklist_names:
            task = asyncio.create_task(self._async_retrieve_picklist(picklist_name))
            tasks.append(task)

        # Wait for all tasks to complete
        result_list = await asyncio.gather(*tasks)

        # Process results
        result_list_processed = []

        for result, picklist_name in zip(result_list, picklist_names):
            if not result.empty:
                result_list_processed.append(result)

        if result_list_processed:
            result = pd.concat(result_list_processed, ignore_index=True)
            return result
        else:
            return pd.DataFrame(
                columns=["name", "label", "status", "id", "picklistName"]
            )

    async def _async_retrieve_picklist(self, picklist_name):
        """
        Helper method for asynchronous picklist value retrieval

        Args:
            picklist_name (str): The API name of the picklist

        Returns:
            pandas.DataFrame: DataFrame containing the picklist values
        """
        try:
            df = self.retrieve_picklist_values(picklist_name)
            return df
        except Exception as e:
            print(f"Error retrieving picklist {picklist_name}: {e}")
            return pd.DataFrame()
