import os
import pandas as pd
from typing import Dict, List, Optional, Union, BinaryIO, Any


class ConfigurationMigrationService:
    """
    Service class for managing configuration migration in Veeva Vault.

    This service provides methods to interact with configuration migration-related API endpoints,
    allowing export, import, validation, and deployment of Vault Packages (VPKs).
    These packages allow you to migrate configuration changes between two Vaults.
    """

    def __init__(self, client):
        """
        Initialize with a VaultClient instance

        Args:
            client: An initialized VaultClient instance for API communication
        """
        self.client = client

    def export_package(self, package_name: str) -> Dict[str, Any]:
        """
        Exports a Vault Package (VPK) from an Outbound Package.

        Corresponds to POST /api/{version}/services/package

        On SUCCESS, the response includes:
        - url: The URL to retrieve the current status of the export job.
        - job_id: The Job ID value used to retrieve the status and results of the request.
        - A separate email with a link to download the .vpk file.

        Args:
            package_name (str): The name of the Outbound Package to export.

        Returns:
            dict: The JSON response containing export job information.
        """
        url = f"api/{self.client.LatestAPIversion}/services/package"
        data = {"packageName": package_name}

        return self.client.api_call(url, method="POST", data=data)

    def import_package(self, file_path: Union[str, BinaryIO]) -> Dict[str, Any]:
        """
        Asynchronously imports and validates a VPK package.

        Corresponds to PUT /api/{version}/services/package

        On completion, Vault sends an email notification which includes a link to the validation log.
        For packages that include Vault Java SDK code, this checks code compilation and restrictions
        in use of the JDK. For example, new is not allowed for non-allowlisted classes.

        On SUCCESS, the response includes:
        - url: The URL to retrieve the current status of the import job.
        - job_id: The Job ID value used to retrieve the status and results of the request.
        - A separate email with a link to download the validation log.

        Args:
            file_path (Union[str, BinaryIO]): The path to the .vpk file or a file-like object.

        Returns:
            dict: The JSON response containing import job information.
        """
        url = f"api/{self.client.LatestAPIversion}/services/package"

        # Handle both file path strings and file-like objects
        if isinstance(file_path, str):
            with open(file_path, "rb") as f:
                files = {"file": (os.path.basename(file_path), f)}
                return self.client.api_call(url, method="PUT", files=files)
        else:
            # Assume file_path is a file-like object
            files = {"file": file_path}
            return self.client.api_call(url, method="PUT", files=files)

    def deploy_package(self, package_id: str) -> Dict[str, Any]:
        """
        Deploys an imported VPK package to the Vault.

        Corresponds to POST /api/{version}/vobject/vault_package__v/{package_id}/actions/deploy

        On SUCCESS, the response includes:
        - url: The URL to retrieve the current status of the export job.
        - job_id: The Job ID value used to retrieve the status and results of the request.

        Args:
            package_id (str): The id field value of the vault_package__v object record used for deployment.

        Returns:
            dict: The JSON response containing deployment job information.
        """
        url = f"api/{self.client.LatestAPIversion}/vobject/vault_package__v/{package_id}/actions/deploy"

        return self.client.api_call(url, method="POST")

    def retrieve_package_deploy_results(self, package_id: str) -> Dict[str, Any]:
        """
        Retrieves the results of a completed package deployment.

        Corresponds to GET /api/{version}/vobject/vault_package__v/{package_id}/actions/deploy/results

        After Vault has finished processing the deploy job, use this method to retrieve
        the results of the completed deployment.

        The deployment_log provides a URL to download the latest version of the deployment log.
        If the deployed package includes datasets, the response also provides the
        data_deployment_log with a URL to download the data deployment log.

        Args:
            package_id (str): The id field value of the vault_package__v object record used for deployment.

        Returns:
            dict: The JSON response containing detailed deployment results.
        """
        url = f"api/{self.client.LatestAPIversion}/vobject/vault_package__v/{package_id}/actions/deploy/results"

        return self.client.api_call(url, method="GET")

    def retrieve_outbound_package_dependencies(self, package_id: str) -> Dict[str, Any]:
        """
        Retrieves all outstanding component dependencies for an outbound package.

        Corresponds to GET /api/{version}/vobjects/outbound_package__v/{package_id}/dependencies

        Outbound packages only include configuration details for the included components.
        Sometimes, a configuration for one component depends on another component which
        you may not have explicitly specified.

        On SUCCESS, the response includes:
        - total_dependencies: The total number of outstanding component dependencies.
        - target_vault_id: The ID of the target Vault for the outbound package.
        - package_name: The name__v value of the outbound package.
        - package_id: The ID of the outbound_package__v record with these outstanding dependencies.
        - url: The Vault API request to add missing dependencies to this outbound package.
        - package_dependencies: This array contains information about each dependency.
          If there are no outstanding dependencies, this array is not returned.

        Args:
            package_id (str): The ID of the outbound_package__v record from which to retrieve dependencies.

        Returns:
            dict: The JSON response containing dependency information.
        """
        url = f"api/{self.client.LatestAPIversion}/vobjects/outbound_package__v/{package_id}/dependencies"

        return self.client.api_call(url, method="GET")

    def query_component_definitions(self, query: str) -> Dict[str, Any]:
        """
        Retrieves MDL or JSON definitions of Vault components using a VQL query.

        Corresponds to POST /api/{version}/query/components

        Retrieves MDL definitions (mdl_definition__v) and JSON definitions (json_definition__v)
        of Vault components using a VQL query on the vault_component__v and
        vault_package_component__v query targets.

        Args:
            query (str): A VQL query on the vault_component__v or vault_package_component__v query targets.
                        The query can be up to 50,000 characters.
                        Example: "SELECT id, mdl_definition__v FROM vault_component__v
                                WHERE component_type__v = 'Reporttype'"

        Returns:
            dict: The JSON response containing the query results.
        """
        url = f"api/{self.client.LatestAPIversion}/query/components"
        data = {"q": query}

        return self.client.api_call(url, method="POST", data=data)

    def compare_vaults(
        self,
        vault_id: str,
        results_type: Optional[str] = "differences",
        details_type: Optional[str] = "simple",
        include_doc_binder_templates: Optional[bool] = True,
        include_vault_settings: Optional[bool] = True,
        component_types: Optional[str] = None,
        generate_outbound_packages: Optional[bool] = False,
    ) -> Dict[str, Any]:
        """
        Compares the configuration of two different Vaults.

        Corresponds to POST /api/{version}/objects/vault/actions/compare

        The Vault you make the request in is the source Vault, and the target Vault
        for the comparison is listed in the body.

        The user who makes the request must be a cross-domain user and must have access
        to the vault_component__v in both Vaults.

        Args:
            vault_id (str): The target Vault id for the comparison.
            results_type (str, optional): Type of results to return.
                                         "complete" - Include all configuration values.
                                         "differences" - Only show differences between Vaults.
                                         Defaults to "differences".
            details_type (str, optional): Level of detail in the comparison.
                                         "none" - Component level details only.
                                         "simple" - Include simple attribute-level details.
                                         "complex" - Show all attribute-level details.
                                         Defaults to "simple".
            include_doc_binder_templates (bool, optional): Whether to include Document and Binder Templates.
                                                         Defaults to True.
            include_vault_settings (bool, optional): Whether to include Vault Settings.
                                                    Defaults to True.
            component_types (str, optional): Comma separated list of component types to include.
                                            Set to "none" to exclude all component types.
                                            Example: "Doclifecycle,Doctype,Workflow"
                                            Defaults to include all components.
            generate_outbound_packages (bool, optional): Whether to automatically generate an Outbound
                                                        Package based on differences. Defaults to False.

        Returns:
            dict: The JSON response containing the comparison job information.
        """
        url = f"api/{self.client.LatestAPIversion}/objects/vault/actions/compare"

        data = {
            "vault_id": vault_id,
            "results_type": results_type,
            "details_type": details_type,
            "include_doc_binder_templates": include_doc_binder_templates,
            "include_vault_settings": include_vault_settings,
            "generate_outbound_packages": generate_outbound_packages,
        }

        if component_types:
            data["component_types"] = component_types

        return self.client.api_call(url, method="POST", data=data)

    def generate_configuration_report(
        self,
        include_vault_settings: Optional[bool] = True,
        include_inactive_components: Optional[bool] = False,
        include_components_modified_since: Optional[str] = None,
        include_doc_binder_templates: Optional[bool] = True,
        suppress_empty_results: Optional[bool] = False,
        component_types: Optional[str] = None,
        output_format: Optional[str] = "Excel_Macro_Enabled",
    ) -> Dict[str, Any]:
        """
        Generates an Excel™ report containing configuration information for a Vault.

        Corresponds to POST /api/{version}/objects/vault/actions/configreport

        Users must have the Vault Configuration Report permission to use this API.

        Args:
            include_vault_settings (bool, optional): Whether to include Vault Settings.
                                                    Defaults to True.
            include_inactive_components (bool, optional): Whether to include inactive components
                                                        and subcomponents. Defaults to False.
                                                        Note: For document workflows, if a workflow
                                                        was active but is currently in "editing" state,
                                                        the report shows the latest active version.
                                                        For object workflows, this setting is respected.
            include_components_modified_since (str, optional): Only include components modified
                                                            since the specified date in format yyyy-mm-dd.
                                                            This option is not available for subcomponents.
            include_doc_binder_templates (bool, optional): Whether to include document and binder templates.
                                                         Defaults to True.
            suppress_empty_results (bool, optional): Whether to exclude tabs with only header rows.
                                                    Defaults to False.
            component_types (str, optional): Comma-separated list of component types to include.
                                            Example: "Doclifecycle,Doctype,Workflow"
                                            Defaults to include all components.
            output_format (str, optional): Output format either "Excel" (XLSX) or
                                          "Excel_Macro_Enabled" (XLSM).
                                          Defaults to "Excel_Macro_Enabled".

        Returns:
            dict: The JSON response containing the configuration report job information.
        """
        url = f"api/{self.client.LatestAPIversion}/objects/vault/actions/configreport"

        data = {
            "include_vault_settings": include_vault_settings,
            "include_inactive_components": include_inactive_components,
            "include_doc_binder_templates": include_doc_binder_templates,
            "suppress_empty_results": suppress_empty_results,
            "output_format": output_format,
        }

        if include_components_modified_since:
            data["include_components_modified_since"] = (
                include_components_modified_since
            )

        if component_types:
            data["component_types"] = component_types

        return self.client.api_call(url, method="POST", data=data)

    def validate_package(self, file_path: Union[str, BinaryIO]) -> Dict[str, Any]:
        """
        Validates a VPK package without importing it.

        Corresponds to POST /api/{version}/services/package/actions/validate

        The validation response includes the same information on dependent components
        as validation logs generated through the UI. For packages that include Vault Java SDK code,
        this checks code compilation and restrictions in use of the JDK.

        This endpoint does not import your package.

        Args:
            file_path (Union[str, BinaryIO]): The path to the .vpk file or a file-like object.

        Returns:
            dict: The JSON response containing detailed validation results.
        """
        url = f"api/{self.client.LatestAPIversion}/services/package/actions/validate"

        # Handle both file path strings and file-like objects
        if isinstance(file_path, str):
            with open(file_path, "rb") as f:
                files = {"file": (os.path.basename(file_path), f)}
                return self.client.api_call(url, method="POST", files=files)
        else:
            # Assume file_path is a file-like object
            files = {"file": file_path}
            return self.client.api_call(url, method="POST", files=files)

    def validate_inbound_package(self, package_id: str) -> Dict[str, Any]:
        """
        Validates an imported VPK package before deploying it to your Vault.

        Corresponds to POST /api/{version}/services/vobject/vault_package__v/{package_id}/actions/validate

        The validation response includes information on dependent components and whether
        they exist in the package or in your Vault. You can then add missing dependencies
        to the package in the source Vault before re-importing and deploying it to your target Vault.

        Args:
            package_id (str): The id field value of the vault_package__v object record to validate.

        Returns:
            dict: The JSON response containing detailed validation results.
        """
        url = f"api/{self.client.LatestAPIversion}/services/vobject/vault_package__v/{package_id}/actions/validate"

        return self.client.api_call(url, method="POST")

    def enable_configuration_mode(self) -> Dict[str, Any]:
        """
        Enables Configuration Mode in the currently authenticated Vault.

        Corresponds to POST /api/{version}/services/configuration_mode/actions/enable

        When enabled, Configuration Mode locks non-Admin users out of the Vault.
        Vault Owners and System Admins can still access the Vault to deploy
        configuration migration packages or set up Dynamic Access Control (DAC).

        Users with access to multiple Vaults can log in if at least one (1) Vault
        in the domain is not in Configuration Mode.

        On SUCCESS, this endpoint enables Configuration Mode in the currently authenticated Vault,
        terminates sessions for any non-Admin users currently logged in, and prevents
        other non-Admin users from logging in. Sessions can take up to five (5) minutes
        to terminate for users accessing the Vault UI and up to 15 minutes for users accessing the API.

        Returns:
            dict: The JSON response confirming Configuration Mode has been enabled.
        """
        url = f"api/{self.client.LatestAPIversion}/services/configuration_mode/actions/enable"

        return self.client.api_call(url, method="POST")

    def disable_configuration_mode(self) -> Dict[str, Any]:
        """
        Disables Configuration Mode in the currently authenticated Vault.

        Corresponds to POST /api/{version}/services/configuration_mode/actions/disable

        When you disable Configuration Mode, non-Admin users can now access the Vault.

        On SUCCESS, this endpoint disables Configuration Mode in the currently
        authenticated Vault. Vault allows non-Admin users to log back in.

        Returns:
            dict: The JSON response confirming Configuration Mode has been disabled.
        """
        url = f"api/{self.client.LatestAPIversion}/services/configuration_mode/actions/disable"

        return self.client.api_call(url, method="POST")
