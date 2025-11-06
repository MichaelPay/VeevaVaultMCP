import json
from typing import Dict, Any, Optional, Union, List
from .base_service import BaseLifecycleWorkflowService


class DocumentLifecycleWorkflowService(BaseLifecycleWorkflowService):
    """
    Service class for handling Veeva Vault document lifecycle and workflow operations.

    This service provides methods for retrieving document user actions, initiating document
    user actions, retrieving and managing document workflows, and more.

    Document lifecycles are the sequences of states (Draft, In Review, etc.) a document goes
    through during its life. A lifecycle can be simple (two states requiring users to manually
    move between states) or very complex (multiple states with different security and workflows
    that automatically move the document to another state).
    """

    def retrieve_document_user_actions(
        self, doc_id: str, major_version: str, minor_version: str
    ) -> Dict[str, Any]:
        """
        Retrieve all available user actions on a specific version of a document which:
        - The authenticated user has permission to view or initiate.
        - Can be initiated through the API.
        - Is not currently in an active workflow.

        GET /api/{version}/objects/documents/{doc_id}/versions/{major_version}/{minor_version}/lifecycle_actions

        Args:
            doc_id: The document id field value from which to retrieve available user actions.
            major_version: The major version number of the document.
            minor_version: The minor version number of the document.

        Returns:
            dict: List of available user actions that can be initiated on the specified version of the document.

        Notes:
            - Each action may include: name__v, label__v, lifecycle_action_type__v, lifecycle__v, state__v,
              executable__v, entry_requirements__v
            - The API allows initiating workflow (legacy), state change, controlled copy, create presentation,
              and create email fragment action types.
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/{doc_id}/versions/{major_version}/{minor_version}/lifecycle_actions"

        headers = {"Accept": "application/json"}

        return self.client.api_call(url, headers=headers)

    def retrieve_user_actions_on_multiple_documents(
        self, doc_ids: str
    ) -> Dict[str, Any]:
        """
        Retrieve all available user actions on specific versions of multiple documents.

        POST /api/{version}/objects/documents/lifecycle_actions

        Args:
            doc_ids: The id and version numbers for each document for which to retrieve
                    the available user actions. Include a comma-separated list of document IDs
                    and major and minor version numbers in the format {doc_id:major_version:minor_version}.
                    For example, "22:0:1,21:1:0,20:1:0".

        Returns:
            dict: List of available lifecycle actions that can be initiated on the specified versions of multiple documents.

        Notes:
            - Each action may include: name__v, label__v, lifecycle_action_type__v, lifecycle__v, state__v,
              entry_requirements__v
            - Lifecycle actions are not returned for documents which are currently in an active workflow.
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/lifecycle_actions"

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }

        data = {"docIds": doc_ids}

        return self.client.api_call(url, method="POST", headers=headers, data=data)

    def retrieve_document_entry_criteria(
        self, doc_id: str, major_version: str, minor_version: str, action_name: str
    ) -> Dict[str, Any]:
        """
        Retrieve the entry criteria for a user action. Entry criteria are requirements the document
        must meet before you can initiate the action.

        GET /api/{version}/objects/documents/{doc_id}/versions/{major_version}/{minor_version}/lifecycle_actions/{name__v}/entry_requirements

        Args:
            doc_id: The document id field value from which to retrieve available user actions.
            major_version: The major version number of the document.
            minor_version: The minor version number of the document.
            action_name: The lifecycle name__v field value from which to retrieve entry criteria.

        Returns:
            dict: List of entry criteria properties that must be met before the action can be initiated.

        Notes:
            - Entry criteria are dynamic and depend on the lifecycle configuration, lifecycle state, or
              any workflow activation requirements defined in the Start Step of the workflow.
            - To retrieve entry criteria, the authenticated user must have permission to execute the action.
            - The response may include metadata elements such as name, description, type,
              objectTypeReferenced, required, editable, repeating, minValue, maxValue, values,
              currentSetting, and scope.
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/{doc_id}/versions/{major_version}/{minor_version}/lifecycle_actions/{action_name}/entry_requirements"

        headers = {"Accept": "application/json"}

        return self.client.api_call(url, headers=headers)

    def initiate_document_user_action(
        self,
        doc_id: str,
        major_version: str,
        minor_version: str,
        action_name: str,
        data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Initiate a user action on a document. Before initiating, you should retrieve any applicable
        entry criteria for the action.

        PUT /api/{version}/objects/documents/{doc_id}/versions/{major_version}/{minor_version}/lifecycle_actions/{name__v}

        Args:
            doc_id: The document id field value on which to initiate the user action.
            major_version: The major version number of the document.
            minor_version: The minor version number of the document.
            action_name: The action name__v field value to initiate.
            data: Data containing required fields for the action.

        Returns:
            dict: API response indicating success or failure. For a workflow action, includes workflow_id__v.

        Notes:
            - Only some user action types can be initiated through the API (workflow, stateChange, etc.).
            - The authenticated user must have permission to initiate this action.
            - For start_legacy_workflow, include required entry criteria fields as name-value pairs.
            - For state_change, required entry criteria must be set on the document prior to this request.
            - The API does not support initiating user actions requiring eSignatures.
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/{doc_id}/versions/{major_version}/{minor_version}/lifecycle_actions/{action_name}"

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }

        return self.client.api_call(
            url, method="PUT", headers=headers, data=data if data else {}
        )

    def download_controlled_copy_job_results(
        self, lifecycle_state_action: str, job_id: str
    ) -> Dict[str, Any]:
        """
        Download the controlled copy after initiating a controlled copy user action.

        This endpoint is intended for use by integrations requesting and routing controlled copies
        of content as a system integrations account on behalf of users.

        GET /api/{version}/objects/documents/actions/{lifecycle_and_state_and_action}/{job_id}/results

        Args:
            lifecycle_state_action: The name__v values for the lifecycle, state, and action
                                   in the format {lifecycle_name}.{state_name}.{action_name}.
            job_id: The ID of the job, returned from the original job request.

        Returns:
            file: Downloaded controlled copy as a file stream.

        Notes:
            - This endpoint is for Extensible Controlled Copy; controlled_copy_trace__v and controlled_copy_user_input__v objects.
            - You must have previously requested an initiate controlled copy job (via the API) which is no longer active
            - You must be the user who initiated the job or have the Admin: Jobs: Read permission
            - On SUCCESS, Vault downloads your controlled copy
            - The HTTP Response Header Content-Type is set to application/octet-stream
            - The HTTP Response Header Content-Disposition contains a default filename component
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/actions/{lifecycle_state_action}/{job_id}/results"

        headers = {"Accept": "application/json"}

        return self.client.api_call(url, headers=headers)

    def initiate_bulk_document_user_actions(
        self,
        action_name: str,
        doc_ids: str,
        lifecycle: str,
        state: str,
        data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Initiate a user action on multiple documents. For each bulk action, you may only select
        a single workflow that Vault will start for all selected and valid documents.

        PUT /api/{version}/objects/documents/lifecycle_actions/{user_action_name}

        Args:
            action_name: The user action name__v field value.
            doc_ids: Comma-separated list of document IDs and major and minor version numbers.
                    For example, "222:0:1,223:0:1,224:0:1,225:0:1".
            lifecycle: Name of the document lifecycle.
            state: Current state of your document.
            data: Additional data required for the action.

        Returns:
            dict: API response indicating success or failure.

        Notes:
            - The user action is only executed on document IDs in the lifecycle and state specified.
            - Document IDs listed which are not in the specified lifecycle and state are skipped.
            - On SUCCESS, the initiating user receives a summary email detailing successes and failures.
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/lifecycle_actions/{action_name}"

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }

        request_data = {"docIds": doc_ids, "lifecycle": lifecycle, "state": state}

        if data:
            request_data.update(data)

        return self.client.api_call(
            url, method="PUT", headers=headers, data=request_data
        )

    def retrieve_binder_user_actions(
        self, binder_id: str, major_version: str, minor_version: str
    ) -> Dict[str, Any]:
        """
        Retrieve all available user actions on a specific version of a binder which:
        - The authenticated user has permission to view or initiate.
        - Can be initiated through the API.
        - Is not currently in an active workflow.

        GET /api/{version}/objects/binders/{binder_id}/versions/{major_version}/{minor_version}/lifecycle_actions

        Args:
            binder_id: The id field value of the binder from which to retrieve available user actions.
            major_version: The major version number of the binder.
            minor_version: The minor version number of the binder.

        Returns:
            dict: List of available user actions that can be initiated on the specified version of the binder.

        Notes:
            - Each action may include: name__v, label__v, lifecycle_action_type__v, lifecycle__v, state__v,
              executable__v, entry_requirements__v
        """
        url = f"api/{self.client.LatestAPIversion}/objects/binders/{binder_id}/versions/{major_version}/{minor_version}/lifecycle_actions"

        headers = {"Accept": "application/json"}

        return self.client.api_call(url, headers=headers)

    def retrieve_user_actions_on_multiple_binders(
        self, binder_ids: str
    ) -> Dict[str, Any]:
        """
        Retrieve all available user actions on specific versions of multiple binders.

        POST /api/{version}/objects/binders/lifecycle_actions

        Args:
            binder_ids: The id and version numbers of binders for which to retrieve the available user actions.
                       Include a comma-separated list of binder IDs and major and minor version numbers
                       in the format {binder_id:major_version:minor_version}. For example, "22:0:1,153:1:0,154:1:0".

        Returns:
            dict: List of available lifecycle actions that can be initiated on the specified versions of multiple binders.

        Notes:
            - Each action may include: name__v, label__v, lifecycle_action_type__v, lifecycle__v, state__v,
              entry_requirements__v
            - Lifecycle actions are not returned for binders which are currently in an active workflow.
        """
        url = f"api/{self.client.LatestAPIversion}/objects/binders/lifecycle_actions"

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }

        data = {"docIds": binder_ids}

        return self.client.api_call(url, method="POST", headers=headers, data=data)

    def retrieve_binder_entry_criteria(
        self, binder_id: str, major_version: str, minor_version: str, action_name: str
    ) -> Dict[str, Any]:
        """
        Retrieve the entry criteria for a user action on a binder. Entry criteria are requirements
        the binder must meet before you can initiate the action.

        GET /api/{version}/objects/binders/{binder_id}/versions/{major_version}/{minor_version}/lifecycle_actions/{name__v}/entry_requirements

        Args:
            binder_id: The binder id field value from which to retrieve available user actions.
            major_version: The major version number of the binder.
            minor_version: The minor version number of the binder.
            action_name: The lifecycle name__v field value from which to retrieve entry criteria.

        Returns:
            dict: List of entry criteria properties that must be met before the action can be initiated.

        Notes:
            - Entry criteria are dynamic and depend on the lifecycle configuration, lifecycle state, or
              any workflow activation requirements defined in the Start Step of the workflow.
            - To retrieve entry criteria, the authenticated user must have permission to execute the action.
            - Response includes metadata elements similar to document entry criteria.
        """
        url = f"api/{self.client.LatestAPIversion}/objects/binders/{binder_id}/versions/{major_version}/{minor_version}/lifecycle_actions/{action_name}/entry_requirements"

        headers = {"Accept": "application/json"}

        return self.client.api_call(url, headers=headers)

    def initiate_binder_user_action(
        self,
        binder_id: str,
        major_version: str,
        minor_version: str,
        action_name: str,
        data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Initiate a user action on a binder. Before initiating, you should retrieve any applicable
        entry criteria for the action.

        PUT /api/{version}/objects/binders/{binder_id}/versions/{major_version}/{minor_version}/lifecycle_actions/{name__v}

        Args:
            binder_id: The binder id field value on which to initiate the user action.
            major_version: The major version number of the binder.
            minor_version: The minor version number of the binder.
            action_name: The action name__v field value to initiate.
            data: Data containing required fields for the action.

        Returns:
            dict: API response indicating success or failure. For a workflow action, includes workflow_id__v.

        Notes:
            - Only some user action types can be initiated through the API.
            - The authenticated user must have permission to initiate this action.
            - The API does not support initiating user actions requiring eSignatures.
        """
        url = f"api/{self.client.LatestAPIversion}/objects/binders/{binder_id}/versions/{major_version}/{minor_version}/lifecycle_actions/{action_name}"

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }

        return self.client.api_call(
            url, method="PUT", headers=headers, data=data if data else {}
        )

    def initiate_bulk_binder_user_actions(
        self,
        action_name: str,
        binder_ids: str,
        lifecycle: str,
        state: str,
        data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Initiate a user action on multiple binders. For each bulk action, you may only select
        a single workflow that Vault will start for all selected and valid binders.

        PUT /api/{version}/objects/binders/lifecycle_actions/{user_action_name}

        Args:
            action_name: The user action name__v field value.
            binder_ids: Comma-separated list of binder IDs and major and minor version numbers.
                       For example, "222:0:1,223:0:1,224:0:1,225:0:1".
            lifecycle: Name of the binder lifecycle.
            state: Current state of your binder.
            data: Additional data required for the action.

        Returns:
            dict: API response indicating success or failure.

        Notes:
            - The user action is only executed on binder IDs in the lifecycle and state specified.
            - Binder IDs listed which are not in the specified lifecycle and state are skipped.
            - On SUCCESS, the initiating user receives a summary email detailing successes and failures.
        """
        url = f"api/{self.client.LatestAPIversion}/objects/binders/lifecycle_actions/{action_name}"

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }

        request_data = {"docIds": binder_ids, "lifecycle": lifecycle, "state": state}

        if data:
            request_data.update(data)

        return self.client.api_call(
            url, method="PUT", headers=headers, data=request_data
        )

    def retrieve_lifecycle_role_assignment_rules(
        self,
        lifecycle: Optional[str] = None,
        role: Optional[str] = None,
        product: Optional[str] = None,
        country: Optional[str] = None,
        study: Optional[str] = None,
        study_country: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Retrieve lifecycle role assignment rules (default & override) from all roles in all lifecycles
        or filtered by specific parameters.

        GET /api/{version}/configuration/role_assignment_rule

        Args:
            lifecycle: Name of the lifecycle from which to retrieve information.
            role: Name of the role from which to retrieve information.
            product: ID/name of a specific product to see product-based override rules.
            country: ID/name of a specific country to see country-based override rules.
            study: ID/name of a specific study to see study-based override rules (eTMF Vaults only).
            study_country: ID/name of a specific study country to see study country-based
                          override rules (eTMF Vaults only).

        Returns:
            dict: List of lifecycle role assignment rules (default & override).

        Notes:
            - The response includes default role assignments and override role assignments when an
              override condition is met.
            - If you filter by override conditions, the response excludes default role assignments.
            - For both standard and custom roles, you can define a subset of users who are allowed
              in the role and define users that Vault automatically assigns to the role at document
              creation or when a workflow starts.
        """
        url = f"api/{self.client.LatestAPIversion}/configuration/role_assignment_rule"

        headers = {"Accept": "application/json"}

        params = {}
        if lifecycle:
            params["lifecycle__v"] = lifecycle
        if role:
            params["role__v"] = role
        if product:
            params["product__v"] = product
        if country:
            params["country__v"] = country
        if study:
            params["study__v"] = study
        if study_country:
            params["study_country__v"] = study_country

        return self.client.api_call(url, params=params, headers=headers)

    def create_lifecycle_role_assignment_override_rules(
        self, rules: Union[Dict[str, Any], List[Dict[str, Any]]]
    ) -> Dict[str, Any]:
        """
        Create lifecycle role assignment override rules.

        POST /api/{version}/configuration/role_assignment_rule

        Args:
            rules: JSON or CSV input with lifecycle role assignment override rules information.

        Returns:
            dict: API response indicating success or failure for each override rule specified.

        Notes:
            - This request can only be used to specify override rules (conditions, users, and groups).
              It cannot be used to create default rules.
            - The input may include override rules for multiple lifecycles and roles.
            - Each role may be configured with multiple override rules.
            - Required fields include lifecycle__v and role__v.
            - Optional fields include product__v, country__v, allowed_users__v, allowed_groups__v,
              allowed_default_users__v, and allowed_default_groups__v.
        """
        url = f"api/{self.client.LatestAPIversion}/configuration/role_assignment_rule"

        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        data = json.dumps(rules)

        return self.client.api_call(url, method="POST", headers=headers, data=data)

    def update_lifecycle_role_assignment_rules(
        self, rules: Union[Dict[str, Any], List[Dict[str, Any]]]
    ) -> Dict[str, Any]:
        """
        Update lifecycle role assignment rules (default & override).

        PUT /api/{version}/configuration/role_assignment_rule

        Args:
            rules: JSON or CSV input with lifecycle role assignment rules information.

        Returns:
            dict: API response indicating success or failure for each default or override rule specified.

        Notes:
            - The input may include rules for multiple lifecycles and roles.
            - Similar field requirements to the POST endpoint.
        """
        url = f"api/{self.client.LatestAPIversion}/configuration/role_assignment_rule"

        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        data = json.dumps(rules)

        return self.client.api_call(url, method="PUT", headers=headers, data=data)

    def delete_lifecycle_role_assignment_override_rules(
        self,
        lifecycle: str,
        role: str,
        product: Optional[str] = None,
        country: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Delete override rules configured on a specific lifecycle role.

        DELETE /api/{version}/configuration/role_assignment_rule

        Args:
            lifecycle: Name of the lifecycle from which to delete override rules.
            role: Name of the role from which to delete override rules.
            product: Object ID or name to delete specific product-based overrides.
            country: Object ID or name to delete specific country-based overrides.

        Returns:
            dict: API response indicating success or failure and number of rules deleted.

        Notes:
            - Can delete all overrides for a lifecycle role or specific object-based overrides.
            - The response includes a count of rules_deleted.
        """
        url = f"api/{self.client.LatestAPIversion}/configuration/role_assignment_rule"

        headers = {"Accept": "application/json"}

        params = {"lifecycle__v": lifecycle, "role__v": role}

        if product:
            params["product__v"] = product
        if country:
            params["country__v"] = country

        return self.client.api_call(
            url, method="DELETE", params=params, headers=headers
        )

    def retrieve_all_document_workflows(self, loc: bool = False) -> Dict[str, Any]:
        """
        Retrieve all available document workflows that can be initiated on a set of documents which:
        - The authenticated user has permissions to view or initiate
        - Can be initiated through the API

        GET /api/{version}/objects/documents/actions

        Args:
            loc: Whether to include localized strings for labels and help text.

        Returns:
            dict: List of available document workflows.

        Notes:
            - Each workflow includes name, label, type, and cardinality
            - For users without the Workflow: Start permission, the response returns an INSUFFICIENT_ACCESS error.
            - Document workflows enable users to send a collection of one or more documents for
              review and approval using a single workflow.
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/actions"

        headers = {"Accept": "application/json"}

        params = {}
        if loc:
            params["loc"] = "true"

        return self.client.api_call(url, params=params, headers=headers)

    def retrieve_document_workflow_details(
        self, workflow_name: str, loc: bool = False
    ) -> Dict[str, Any]:
        """
        Retrieve the details for a specific document workflow.

        GET /api/{version}/objects/documents/actions/{workflow_name}

        Args:
            workflow_name: The document workflow name value.
            loc: Whether to include localized strings for labels and help text.

        Returns:
            dict: Details about the document workflow including any required prompts.

        Notes:
            - The response lists the fields that must be configured with values to initiate the workflow.
            - These are based on the controls configured in the workflow start step.
            - The response may include control types like prompts, instructions, participant,
              date, documents, description, and variable.
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/actions/{workflow_name}"

        headers = {"Accept": "application/json"}

        params = {}
        if loc:
            params["loc"] = "true"

        return self.client.api_call(url, params=params, headers=headers)

    def initiate_document_workflow(
        self, workflow_name: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Initiate a document workflow on a set of documents.

        POST /api/{version}/objects/documents/actions/{workflow_name}

        Args:
            workflow_name: The document workflow name value.
            data: Data containing required fields for the workflow, such as documents__sys,
                 description__sys, and any participants.

        Returns:
            dict: API response containing record_url, record_id__v, and workflow_id.

        Notes:
            - If any document is not in the relevant state or does not meet configured field conditions,
              the API returns INVALID_DATA and the workflow does not start.
            - Maximum 100 documents can be included in the documents__sys parameter.
            - To add participants, add the name of the participant control with a comma-separated list of
              user and group IDs in the format {user_or_group}:{id}.
            - The description__sys field is typically required and has a maximum of 128 characters.
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/actions/{workflow_name}"

        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        return self.client.api_call(url, method="POST", headers=headers, data=data)
