import pandas as pd
import asyncio


class SandboxVaultsService:
    """
    Service class for managing sandbox Vaults and snapshots in Veeva Vault.

    This service provides methods to interact with all sandbox-related API endpoints,
    allowing retrieval, creation, refreshing, and deletion of sandbox Vaults,
    as well as managing sandbox snapshots and pre-production Vaults.
    """

    def __init__(self, client):
        """
        Initialize with a VaultClient instance

        Args:
            client: An initialized VaultClient instance for API communication
        """
        self.client = client

    def retrieve_sandboxes(self):
        """
        Retrieves all sandbox Vaults for the authenticated Vault.

        Corresponds to GET /api/{version}/objects/sandbox

        Returns:
            dict: The JSON response containing information about sandbox Vaults with the following fields:
                - entitlements: List of sandbox entitlements, including:
                  - size: The size of the sandbox (Small, Medium, Large, Very Large, Extra Large, or Full)
                  - available: Number of available sandboxes of this size
                  - allowed: Total number of allowed sandboxes of this size
                  - temporary: Number of temporary entitlements (shown only when a temporary entitlement is active)
                - active: List of active sandbox Vaults, each containing:
                  - pod: The name of the POD the sandbox is on
                  - vault_id: The sandbox ID number
                  - name: The name of the sandbox
                  - type: The type of sandbox (e.g., config)
                  - size: The size of the sandbox
                  - status: The current status of the sandbox (building, active, inactive, deleting)
                  - domain: The sandbox domain
                  - dns: The sandbox domain name
                  - source_vault_id: The Vault ID of the sandbox's parent Vault
                  - refresh_available: The date and time when this sandbox can be refreshed
                  - created_date: The date and time when the sandbox was created
                  - created_by: The user ID of the creator
                  - modified_date: The date and time when the sandbox was last modified
                  - modified_by: The user ID of the modifier
                  - entitlements: The sandbox entitlements
                  - release: The type of release (general, limited, or prerelease)
                  - expiration_date: The expiration date of the sandbox Vault (NULL if never expires)
        """
        url = f"api/{self.client.LatestAPIversion}/objects/sandbox"
        return self.client.api_call(url)

    def retrieve_sandbox_details(self, vault_id):
        """
        Retrieves information about the sandbox for the given Vault ID.

        Corresponds to GET /api/{version}/objects/sandbox/{vault_id}

        Args:
            vault_id (int): The Vault ID of the sandbox

        Returns:
            dict: The JSON response containing detailed information about the sandbox Vault with the following fields:
                - pod: The name of the POD the sandbox is on
                - vault_id: The sandbox ID number
                - name: The name of the sandbox
                - type: The type of sandbox (e.g., config)
                - size: The size of the sandbox (Small, Medium, Large, Very Large, Extra Large, or Full)
                - status: The current status of the sandbox (building, active, inactive, deleting)
                - domain: The sandbox domain
                - dns: The sandbox domain name
                - source_vault_id: The Vault ID of the sandbox's parent Vault
                - refresh_available: The date and time when this sandbox can be refreshed
                - created_date: The date and time when the sandbox was created
                - created_by: The user ID of the creator
                - modified_date: The date and time when the sandbox was last modified
                - modified_by: The user ID of the modifier
                - limits: Sandbox limits (e.g., total_object_records, document_versions)
                  - name: The name of the limit
                  - used: The amount used
                  - allowed: The total allowed
                - entitlements: The sandbox entitlements
                - release: The type of release (general, limited, or prerelease)
                - expiration_date: The expiration date of the sandbox Vault (NULL if never expires)
        """
        url = f"api/{self.client.LatestAPIversion}/objects/sandbox/{vault_id}"
        return self.client.api_call(url)

    def recheck_sandbox_usage_limit(self):
        """
        Recalculates the usage values of the sandbox Vaults for the authenticated Vault.

        Corresponds to POST /api/{version}/objects/sandbox/actions/recheckusage

        This action can be initiated up to 100 times in a 24-hour period.
        In the UI, this information is available in Admin > Settings.

        Returns:
            dict: The API response indicating success or failure
        """
        url = f"api/{self.client.LatestAPIversion}/objects/sandbox/actions/recheckusage"
        return self.client.api_call(url, method="POST")

    def change_sandbox_size(self, changes):
        """
        Changes the size of one or more sandbox Vaults for the authenticated Vault.

        Corresponds to POST /api/{version}/objects/sandbox/batch/changesize

        You can initiate this action if there are sufficient allowances and the current
        sandbox meets the data and user limits of the requested size.

        Args:
            changes (list): List of dictionaries, each containing:
                - name (str): The name of the sandbox Vault
                - size (str): The requested size of the sandbox
                  (Small, Medium, Large, Very Large, Extra Large, or Full)

        Returns:
            dict: The API response indicating success or failure
                - responseStatus: "SUCCESS" if successful
                - responseMessage: A message indicating the operation result
                - errorCodes: Error codes if any
                - errorType: Error type if any
        """
        url = f"api/{self.client.LatestAPIversion}/objects/sandbox/batch/changesize"
        return self.client.api_call(url, method="POST", json=changes)

    def set_sandbox_entitlements(
        self, name, size, allowance, grant, temporary_allowance=None
    ):
        """
        Sets new sandbox entitlements, including granting and revoking allowances, for the given sandbox name.

        Corresponds to POST /api/{version}/objects/sandbox/entitlements/set

        Args:
            name (str): The name of the sandbox Vault
            size (str): The size of the sandbox (Small, Medium, Large, Very Large, Extra Large, or Full)
            allowance (int): The number of entitlements to grant or revoke
            grant (bool): True to grant allowances, False to revoke them
            temporary_allowance (int, optional): The number of temporary sandbox allowances to grant or revoke

        Returns:
            dict: The API response containing the updated entitlements:
                - responseStatus: "SUCCESS" if successful
                - data: Dictionary containing entitlements information
                  - entitlements: List of sandbox entitlements with size, available, allowed, and temporary values
        """
        url = f"api/{self.client.LatestAPIversion}/objects/sandbox/entitlements/set"
        data = {
            "name": name,
            "size": size,
            "allowance": allowance,
            "grant": "true" if grant else "false",
        }

        if temporary_allowance is not None:
            data["temporary_allowance"] = temporary_allowance

        return self.client.api_call(url, method="POST", data=data)

    def create_or_refresh_sandbox(
        self,
        name,
        size,
        domain,
        type=None,
        source=None,
        source_snapshot=None,
        add_requester=None,
        release=None,
    ):
        """
        Creates a new sandbox or refreshes an existing sandbox for the currently authenticated Vault.

        Corresponds to POST /api/{version}/objects/sandbox

        Providing a name which already exists will refresh the existing sandbox Vault.
        You can also refresh a sandbox from a snapshot by providing the source_snapshot parameter.

        Args:
            name (str): The name of the sandbox Vault, which appears on the My Vaults page
            size (str): The size of the sandbox (Small, Medium, Large, Very Large, Extra Large, or Full)
            domain (str): The domain to use for the new sandbox (must be lower-case and include domain extension)
            type (str, optional): The type of sandbox, such as config
            source (str, optional): The source to refresh the sandbox from: vault or snapshot
            source_snapshot (str, optional): If the source is a snapshot, provide the api_name of the snapshot
            add_requester (bool, optional): Add the authenticated user as a Vault Owner (defaults to true)
            release (str, optional): The type of release (general, limited, or prerelease)

        Returns:
            dict: The API response containing:
                - responseStatus: "SUCCESS" if successful
                - job_id: The Job ID value to retrieve the status and results of the sandbox creation request
                - url: URL to retrieve the current status of the sandbox creation request
        """
        url = f"api/{self.client.LatestAPIversion}/objects/sandbox"
        data = {"name": name, "size": size, "domain": domain}

        if type:
            data["type"] = type
        if source:
            data["source"] = source
        if source_snapshot:
            data["source_snapshot"] = source_snapshot
        if add_requester is not None:
            data["add_requester"] = "true" if add_requester else "false"
        if release:
            data["release"] = release

        return self.client.api_call(url, method="POST", data=data)

    def refresh_sandbox_from_snapshot(self, vault_id, source_snapshot):
        """
        Refreshes a sandbox Vault in the currently authenticated Vault from an existing snapshot.

        Corresponds to POST /api/{version}/objects/sandbox/{vault_id}/actions/refresh

        Args:
            vault_id (int): The Vault ID of the sandbox to be refreshed
            source_snapshot (str): The api_name of the snapshot to refresh the sandbox from

        Returns:
            dict: The API response containing:
                - responseStatus: "SUCCESS" if successful
                - job_id: The Job ID value to retrieve the status and results of the sandbox refresh request
                - url: URL to retrieve the current status of the sandbox refresh request
        """
        url = f"api/{self.client.LatestAPIversion}/objects/sandbox/{vault_id}/actions/refresh"
        data = {"source_snapshot": source_snapshot}

        return self.client.api_call(url, method="POST", data=data)

    def delete_sandbox(self, name):
        """
        Deletes a sandbox Vault.

        Corresponds to DELETE /api/{version}/objects/sandbox/{name}

        How often you can delete a Vault depends on its size.

        Args:
            name (str): The name of the sandbox Vault to delete

        Returns:
            dict: The API response containing:
                - responseStatus: "SUCCESS" if successful
                - responseMessage: A message indicating the operation result
        """
        url = f"api/{self.client.LatestAPIversion}/objects/sandbox/{name}"
        return self.client.api_call(url, method="DELETE")

    def create_sandbox_snapshot(
        self, source_sandbox, name, description=None, include_data=False
    ):
        """
        Creates a new sandbox snapshot for the indicated sandbox Vault.

        Corresponds to POST /api/{version}/objects/sandbox/snapshot

        Args:
            source_sandbox (str): The name of the sandbox Vault to take a snapshot of
            name (str): The name of the new snapshot
            description (str, optional): The description of the new snapshot
            include_data (bool, optional): Set to True to include data as part of the snapshot,
                                           False to include only configuration (default)

        Returns:
            dict: The API response containing:
                - responseStatus: "SUCCESS" if successful
                - job_id: The Job ID value to retrieve the status and results of the snapshot creation request
                - url: URL to retrieve the current status of the snapshot creation request
        """
        url = f"api/{self.client.LatestAPIversion}/objects/sandbox/snapshot"
        data = {
            "source_sandbox": source_sandbox,
            "name": name,
            "include_data": "true" if include_data else "false",
        }

        if description:
            data["description"] = description

        return self.client.api_call(url, method="POST", data=data)

    def retrieve_sandbox_snapshots(self):
        """
        Retrieves information about sandbox snapshots managed by the authenticated Vault.

        Corresponds to GET /api/{version}/objects/sandbox/snapshot

        Returns:
            dict: The JSON response containing information about snapshots with the following fields:
                - available: The number of available snapshots
                - snapshots: List of snapshots, each containing:
                  - name: The name of the snapshot
                  - api_name: The API name of the snapshot
                  - type: The type of the source sandbox
                  - description: The description of the snapshot
                  - status: The current status of the snapshot (building, active, maintenance, deleted)
                  - upgrade_status: The current upgrade status of the snapshot
                    (Good, Upgrade Required, Upgrade Available, Expired)
                  - source_sandbox: The name of the sandbox Vault the snapshot was created from
                  - total_object_records: The total number of object records in the snapshot
                  - document_versions: The total number of document versions in the snapshot
                  - vault_version: The release version of the source sandbox Vault when the snapshot was created
                  - update_available: The date and time when the snapshot can next be updated
                  - created_date: The date and time when the snapshot was created
                  - expiration_date: The date and time when the snapshot will expire
                  - domain: The domain of the source sandbox Vault
                  - created_by: The user ID of the creator
        """
        url = f"api/{self.client.LatestAPIversion}/objects/sandbox/snapshot"
        return self.client.api_call(url)

    def delete_sandbox_snapshot(self, api_name):
        """
        Deletes a sandbox snapshot managed by the authenticated Vault.

        Corresponds to DELETE /api/{version}/objects/sandbox/snapshot/{api_name}

        Deleted snapshots cannot be recovered.

        Args:
            api_name (str): The API name of the snapshot

        Returns:
            dict: The API response indicating success or failure:
                - responseStatus: "SUCCESS" if successful
        """
        url = f"api/{self.client.LatestAPIversion}/objects/sandbox/snapshot/{api_name}"
        return self.client.api_call(url, method="DELETE")

    def update_sandbox_snapshot(self, api_name):
        """
        Recreates a sandbox snapshot for the same source sandbox Vault.

        Corresponds to POST /api/{version}/objects/sandbox/snapshot/{api_name}/actions/update

        This request replaces the existing snapshot with the newly created one.

        Args:
            api_name (str): The API name of the snapshot

        Returns:
            dict: The API response containing:
                - responseStatus: "SUCCESS" if successful
                - job_id: The Job ID value to retrieve the status and results of the snapshot update request
                - url: URL to retrieve the current status of the snapshot update request
        """
        url = f"api/{self.client.LatestAPIversion}/objects/sandbox/snapshot/{api_name}/actions/update"
        return self.client.api_call(url, method="POST")

    def upgrade_sandbox_snapshot(self, api_name):
        """
        Upgrades a sandbox snapshot to match the release version of the source sandbox Vault.

        Corresponds to POST /api/{version}/objects/sandbox/snapshot/{api_name}/actions/upgrade

        Your request to upgrade a snapshot is only valid if the upgrade_status is 'Upgrade Available'
        or 'Upgrade Required'.

        Args:
            api_name (str): The API name of the snapshot

        Returns:
            dict: The API response containing:
                - responseStatus: "SUCCESS" if successful
                - job_id: The Job ID value to retrieve the status and results of the snapshot upgrade request
                - url: URL to retrieve the current status of the snapshot upgrade request
        """
        url = f"api/{self.client.LatestAPIversion}/objects/sandbox/snapshot/{api_name}/actions/upgrade"
        return self.client.api_call(url, method="POST")

    def build_production_vault(self, source):
        """
        Builds a production Vault from a pre-production Vault.

        Corresponds to POST /api/{version}/objects/sandbox/actions/buildproduction

        Given a pre-production Vault, build a production Vault. This is analogous to the Build
        action in the Vault UI. After building your Vault, you can promote it to production.

        You can build or rebuild the source Vault for a given pre-production Vault no more than
        three times in a 24 hour period.

        Args:
            source (str): The name of the source Vault to build (current pre-production Vault or sandbox)

        Returns:
            dict: The API response containing:
                - responseStatus: "SUCCESS" if successful
                - job_id: The Job ID value to retrieve the status and results of the production build request
                - url: URL to retrieve the current status of the production build request
        """
        url = f"api/{self.client.LatestAPIversion}/objects/sandbox/actions/buildproduction"
        data = {"source": source}

        return self.client.api_call(url, method="POST", data=data)

    def promote_to_production(self, name):
        """
        Promotes a built pre-production Vault to a production Vault.

        Corresponds to POST /api/{version}/objects/sandbox/actions/promoteproduction

        Given a built pre-production Vault, promote it to a production Vault. This is analogous to
        the Promote action in the Vault UI.

        You must build your pre-production Vault before you can promote it to production.

        Args:
            name (str): The name of the pre-production Vault to promote

        Returns:
            dict: The API response indicating success or failure:
                - responseStatus: "SUCCESS" if successful
        """
        url = f"api/{self.client.LatestAPIversion}/objects/sandbox/actions/promoteproduction"
        data = {"name": name}

        return self.client.api_call(url, method="POST", data=data)
