import json
from .base_service import BaseBinderService


class BinderBindingRulesService(BaseBinderService):
    """
    Service class for managing binding rules on binders in Veeva Vault
    """

    def update_binding_rule(
        self, binder_id, binding_rule__v=None, binding_rule_override__v=None
    ):
        """
        Updates a binding rule for a binder.

        PUT /api/{version}/objects/binders/{binder_id}/binding_rule

        Args:
            binder_id (str): The binder id field value.
            binding_rule__v (str, optional): Indicates which binding rule to apply (which document versions
                to link to the section). Options are: default (bind to the latest available version
                (assumed if binding_rule is blank)), steady-state (bind to latest version in a steady-state),
                or current (bind to current version).
            binding_rule_override__v (bool, optional): Set to true or false to indicate if the specified
                binding rule should override documents or sections which already have binding rules set.
                If set to true, the binding rule is applied to all documents and sections within the
                current section. If blank or set to false, the binding rule is applied only to documents
                and sections within the current section that do not have a binding rule specified.

        Returns:
            dict: On SUCCESS, Vault returns the ID of the updated binder.
                  Example: {"responseStatus": "SUCCESS", "id": 566}
        """
        url = f"api/{self.client.LatestAPIversion}/objects/binders/{binder_id}/binding_rule"

        # Documentation specifies Content-Type should be application/x-www-form-urlencoded
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }

        data = {}
        if binding_rule__v:
            data["binding_rule__v"] = binding_rule__v
        if binding_rule_override__v is not None:
            data["binding_rule_override__v"] = binding_rule_override__v

        # Should use form-encoded data, not JSON
        return self.client.api_call(url, method="PUT", headers=headers, data=data)

    def update_binder_section_binding_rule(
        self, binder_id, node_id, binding_rule__v=None, binding_rule_override__v=None
    ):
        """
        Updates a binding rule for a specific section in a binder.

        PUT /api/{version}/objects/binders/{binder_id}/sections/{node_id}/binding_rule

        Args:
            binder_id (str): The binder id field value.
            node_id (str): The binder node id field value.
            binding_rule__v (str, optional): Indicates which binding rule to apply (which document versions
                to link to the section). Options are: default (bind to the latest available version
                (assumed if binding_rule is blank)), steady-state (bind to latest version in a steady-state),
                or current (bind to current version).
            binding_rule_override__v (bool, optional): Set to true or false to indicate if the specified
                binding rule should override documents or sections which already have binding rules set.
                If set to true, the binding rule is applied to all documents and sections within the
                current section. If blank or set to false, the binding rule is applied only to documents
                and sections within the current section that do not have a binding rule specified.

        Returns:
            dict: On SUCCESS, Vault returns the Node ID of the updated section.
                  Example: {"responseStatus": "SUCCESS", "id": "1427491342404:-1828014479"}
        """
        url = f"api/{self.client.LatestAPIversion}/objects/binders/{binder_id}/sections/{node_id}/binding_rule"

        # Documentation specifies Content-Type should be application/x-www-form-urlencoded
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }

        data = {}
        if binding_rule__v:
            data["binding_rule__v"] = binding_rule__v
        if binding_rule_override__v is not None:
            data["binding_rule_override__v"] = binding_rule_override__v

        # Should use form-encoded data, not JSON
        return self.client.api_call(url, method="PUT", headers=headers, data=data)

    def update_binder_document_binding_rule(
        self,
        binder_id,
        node_id,
        binding_rule__v=None,
        major_version_number__v=None,
        minor_version_number__v=None,
    ):
        """
        Updates a binding rule for a specific document in a binder.

        PUT /api/{version}/objects/binders/{binder_id}/documents/{node_id}/binding_rule

        Args:
            binder_id (str): The binder id field value.
            node_id (str): The binder node id field value.
            binding_rule__v (str, optional): Indicates which binding rule to apply (which document versions
                to link to the section). Options are: default (bind to the latest available version
                (assumed if binding_rule is blank)), steady-state (bind to latest version in a steady-state),
                current (bind to current version), or specific (bind to a specific version).
            major_version_number__v (str, optional): If binding_rule__v=specific, then this is required and
                indicates the major version of the document to be linked. Otherwise it is ignored.
            minor_version_number__v (str, optional): If binding_rule__v=specific, then this is required and
                indicates the minor version of the document to be linked. Otherwise it is ignored.

        Returns:
            dict: On SUCCESS, Vault returns the Node ID of the updated document node within the binder.
                  Example: {"responseStatus": "SUCCESS", "id": "1427491342404:-1828014479"}
        """
        url = f"api/{self.client.LatestAPIversion}/objects/binders/{binder_id}/documents/{node_id}/binding_rule"

        # Documentation specifies Content-Type should be application/x-www-form-urlencoded
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }

        data = {}
        if binding_rule__v:
            data["binding_rule__v"] = binding_rule__v
        if major_version_number__v is not None:
            data["major_version_number__v"] = major_version_number__v
        if minor_version_number__v is not None:
            data["minor_version_number__v"] = minor_version_number__v

        # Should use form-encoded data, not JSON
        return self.client.api_call(url, method="PUT", headers=headers, data=data)
