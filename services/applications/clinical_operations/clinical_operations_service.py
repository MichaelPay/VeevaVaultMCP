from typing import Dict, Any, Optional, Union, BinaryIO
import json


class ClinicalOperationsService:
    """
    Service class for interacting with the Veeva Vault Clinical Operations application.

    This service provides methods for working with EDLs, milestones, procedures,
    site fees, and other Clinical Operations functionality.
    """

    def __init__(self, client):
        """
        Initialize the ClinicalOperationsService with a VaultClient instance.

        Args:
            client: An initialized VaultClient instance for API communication
        """
        self.client = client

    def create_edls(
        self,
        study_id: str,
        data: Any,
        content_type: str = "text/csv",
        accept: str = "text/csv",
        apply_where_edl_items_exist: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """
        Create a new Expected Document List.

        The maximum CSV input file size is 1GB.
        The values in the input must be UTF-8 encoded.
        CSVs must follow the standard RFC 4180 format, with some exceptions.
        The maximum batch size is 500.

        Args:
            study_id: The ID of the study.
            data: The CSV data for the EDL items.
            content_type: Content type of the request data (default: "text/csv").
            accept: Accepted response format (default: "text/csv").
            apply_where_edl_items_exist: If set to true, the Create EDL job is applied to existing EDLs.
                If omitted, defaults to false. This is analogous to the "Apply template where
                expected documents already exist" option in the Vault UI.

        Returns:
            API response containing job_id, url, and response status
        """
        endpoint = f"api/{self.client.LatestAPIversion}/vobjects/study__v/{study_id}/actions/etmfcreateedl"

        params = {}
        if apply_where_edl_items_exist is not None:
            params["applyWhereEdlItemsExist"] = apply_where_edl_items_exist

        headers = {
            "Content-Type": content_type,
            "Accept": accept,
        }

        return self.client.api_call(
            endpoint=endpoint, method="POST", headers=headers, data=data, params=params
        )

    def recalculate_milestone_document_field(self, data: Any) -> Dict[str, Any]:
        """
        Recalculate the milestone__v field on a specified set of documents.

        The maximum CSV input file size is 1GB.
        The values in the input must be UTF-8 encoded.
        CSVs must follow the standard RFC 4180 format, with some exceptions.
        The maximum batch size is 500.

        Args:
            data: CSV data containing document id values in an 'id' column.
                Invalid values or invalid columns are ignored.

        Returns:
            API response containing response status and message
        """
        endpoint = f"api/{self.client.LatestAPIversion}/objects/documents/milestones/actions/recalculate"

        headers = {
            "Content-Type": "text/csv",
            "Accept": "application/json",
        }

        return self.client.api_call(
            endpoint=endpoint, method="POST", headers=headers, data=data
        )

    def apply_edl_template_to_milestone(
        self, milestone_id: str, edl_id: str
    ) -> Dict[str, Any]:
        """
        Apply an EDL template to a Milestone object record.

        Args:
            milestone_id: The ID of the milestone.
            edl_id: The ID of the EDL template to apply to this milestone.

        Returns:
            API response containing job_id, url, and response status
        """
        endpoint = f"api/{self.client.LatestAPIversion}/vobjects/milestone__v/{milestone_id}/actions/etmfcreateedl"

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }

        data = {"edl_id": edl_id}

        return self.client.api_call(
            endpoint=endpoint, method="POST", headers=headers, data=data
        )

    def create_milestones_from_template(
        self, object_name: str, object_record_id: str
    ) -> Dict[str, Any]:
        """
        Use this request to initiate the Create Milestones from Template user action on a study, study country, or site.

        Args:
            object_name: The object name__v field value. This endpoint only works with the
                study__v, study_country__v, or site__v objects.
            object_record_id: The object record ID field value.

        Returns:
            API response containing job_id, url, and response status
        """
        endpoint = f"api/{self.client.LatestAPIversion}/vobjects/{object_name}/{object_record_id}/actions/createmilestones"

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }

        return self.client.api_call(endpoint=endpoint, method="POST", headers=headers)

    def execute_milestone_story_events(
        self, object_name: str, data: Any, id_param: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Use this request to create Milestones based on specific Story Events for multiple studies, study countries, or sites.
        You can include up to 500 rows in the CSV input.

        Args:
            object_name: The object name__v field value. This endpoint only works with the
                study__v, study_country__v, or site__v objects.
            data: CSV data containing the milestone story event details.
                The CSV file must have columns: id, story_event__v
            id_param: Optional parameter to identify objects in your input by a unique field.
                You can use any object field which has unique set to true in the object metadata,
                with the exception of picklists.

        Returns:
            API response containing success/failure status for each record
        """
        endpoint = f"api/{self.client.LatestAPIversion}/app/clinical/milestone/{object_name}/actions/applytemplate"

        if id_param:
            endpoint += f"?idParam={id_param}"

        headers = {
            "Content-Type": "text/csv",
            "Accept": "text/csv",
        }

        return self.client.api_call(
            endpoint=endpoint, method="POST", headers=headers, data=data
        )

    def generate_milestone_documents(self, data: Any) -> Dict[str, Any]:
        """
        Generate Milestone Document records for up to 500 milestones. Milestone Document records
        are used to display matched document details in the Milestone Workspace.

        Learn more about the Milestone Workplace in Vault Help.

        Args:
            data: CSV data with a single column with the header 'id'. List each milestone ID
                 on a separate row below. Including more than 500 rows results in an error.

        Returns:
            API response indicating success or failure
        """
        endpoint = f"api/{self.client.LatestAPIversion}/app/clinical/milestone/actions/generatemilestonedocuments"

        headers = {
            "Content-Type": "text/csv",
        }

        return self.client.api_call(
            endpoint=endpoint, method="POST", headers=headers, data=data
        )

    def distribute_to_sites(self, safety_distribution_id: str) -> Dict[str, Any]:
        """
        This API allows sponsors and CROs to send Safety reports and letters to Sites.
        Learn more about Safety Distributions in Vault Help.

        Args:
            safety_distribution_id: The record ID of the Safety Distribution record to send.
                Must be in a Ready or Distributed state.

        Returns:
            API response containing job_id and message
        """
        endpoint = f"api/{self.client.LatestAPIversion}/app/clinical/safety_distributions/{safety_distribution_id}/actions/send"

        headers = {
            "Accept": "application/json",
        }

        return self.client.api_call(endpoint=endpoint, method="POST", headers=headers)

    def populate_site_fee_definitions(
        self,
        target_study: str,
        source_study: Optional[list] = None,
        source_template: Optional[list] = None,
    ) -> Dict[str, Any]:
        """
        Given an existing study with Site Fee Definitions or an eligible Site Fee Template,
        automatically generate Site Fee Definitions for a new target study.
        This endpoint is only available in CTMS Vaults with the Veeva Payments add-on.

        Args:
            target_study: The new study to populate with Site Fee Definitions.
            source_study: Optional: To copy the Site Fee Definitions from studies,
                include an array with the study IDs. You must choose either source_study
                or source_template.
            source_template: Optional: To copy the Site Fee Definitions from Site Fee Templates,
                include an array with the template IDs. You must choose either source_study
                or source_template.

        Returns:
            API response with status and details of the operation
        """
        endpoint = f"api/{self.client.LatestAPIversion}/app/clinical/payments/populate-site-fee-definitions"

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        data = {"target_study": target_study}

        if source_study:
            data["source_study"] = source_study
        if source_template:
            data["source_template"] = source_template

        return self.client.api_call(
            endpoint=endpoint, method="POST", headers=headers, json=data
        )

    def initiate_clinical_record_merge(
        self, object_name: str, data: Union[list, Any]
    ) -> Dict[str, Any]:
        """
        Initiate a record merge operation in bulk to eliminate duplicate Global Directory data
        in your Clinical Operations Vault. When merging two records together, you must select
        one record to be the main_record_id and one record to be the duplicate_record_id.
        The merging process updates all inbound references (including attachments) from other
        objects that point to the duplicate record and moves those over to the main record.
        Field values on the main record are not changed, and when the process is complete,
        the duplicate record is deleted. Record merges do not trigger record triggers.

        You can only merge two records together in a single operation, one main record and
        one duplicate record. This is called a merge set. If you have multiple duplicate
        records you wish to merge into the same main record, you need to create multiple
        merge sets and execute multiple record merges.

        The values in the input must be UTF-8 encoded.
        CSVs must follow the standard RFC 4180 format, with some exceptions.
        The maximum batch size is 10 merge sets.
        The maximum number of concurrent merge requests is 500.

        This request only supports record merges for the following objects:
        - Person (person__sys)
        - Organization (organization__v)
        - Location (location__v)
        - Contact Information (contact_information__clin)

        Each object above must have Enable Merges configured and the initiating user must
        have the Application: Object: Merge Records permission. To merge records for other
        objects in your Vault, use Initiate Record Merge. Learn more about record merges
        for Clinical Operations in Vault Help.

        Args:
            object_name: The name of the object to merge. Possible values are person__sys,
                        organization__v, location__v, and contact_information__clin.
            data: JSON or CSV data containing the merge operations. Upload parameters as a
                  JSON or CSV file. You can merge up to 10 merge sets at once. Each entry
                  must contain:
                  - duplicate_record_id (required): The ID of the duplicate record. Each
                    duplicate_record_id can only be merged into one main_record_id record.
                    When the merging process is complete, Vault deletes this record.
                  - main_record_id (required): The ID of the main record. The merging process
                    updates all inbound references (including attachments) from other objects
                    that point to the duplicate record and moves those over to the main record.
                    Vault does not change field values on the main record.

        Returns:
            API response containing jobID for successful operation
        """
        endpoint = f"api/{self.client.LatestAPIversion}/app/clinical/objects/{object_name}/actions/merge"

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        return self.client.api_call(
            endpoint=endpoint, method="POST", headers=headers, json=data
        )

    def enable_study_migration_mode(self, data: list) -> Dict[str, Any]:
        """
        Enable Study Migration Mode for multiple Study records. Sending a request to this
        endpoint initiates a job to set the study_migration__v field on Study records and
        their related object records with the value m__v. You can enable Study Migration
        Mode for up to 500 Study records in a single request.

        When a Study enters Study Migration Mode, Vault makes study-related object data
        for that study hidden and uneditable for non-Admin users. Study Migration Mode
        also bypasses record triggers for the target studies, such as calculating metrics
        and generating related records. Learn more about status and archiving studies in
        Vault Help. Learn more about Clinical Study Migrations.

        Args:
            data: A list of dictionaries containing Study record IDs:
                  - id (required): The ID of the Study record.

        Returns:
            API response containing jobID and url for successful operation
        """
        endpoint = f"api/{self.client.LatestAPIversion}/app/clinical/studies/actions/enable_migration_mode"

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        return self.client.api_call(
            endpoint=endpoint, method="POST", headers=headers, json=data
        )

    def disable_study_migration_mode(self, data: list) -> Dict[str, Any]:
        """
        Disable Study Migration Mode for multiple Study records. Sending a request to this
        endpoint initiates a job to clear the study_migration__v field on Study records and
        their related object records. You can disable Study Migration Mode for up to 500
        Study records in a single request.

        Learn more about status and archiving studies in Vault Help. Learn more about
        Clinical Study Migrations.

        Args:
            data: A list of dictionaries containing Study record IDs:
                  - id (required): The ID of the Study record.

        Returns:
            API response containing jobID and url for successful operation
        """
        endpoint = f"api/{self.client.LatestAPIversion}/app/clinical/studies/actions/disable_migration_mode"

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        return self.client.api_call(
            endpoint=endpoint, method="POST", headers=headers, json=data
        )

    def retrieve_opendata_clinical_affiliations(
        self, object_name: str, record_id: str, accept: str = "application/json"
    ) -> Dict[str, Any]:
        """
        Given a Person or Organization mapped to OpenData Clinical, retrieves contact
        information associated with the Investigator Site record.

        This API returns a maximum of 100 records. If there are more than 100 records to
        return, Vault truncates records beyond 100 in the returned response. To retrieve
        more than 100 records, use Direct Data API.

        Args:
            object_name: The name of the object to merge. Possible values are person__sys,
                        organization__v, location__v, and contact_information__clin.
            record_id: The ID of the person__sys or organization__v record.
            accept: Accepted response format (default: "application/json"). Can also be "text/csv".

        Returns:
            API response containing information about the Person or Organization mapped to
            OpenData Clinical
        """
        endpoint = f"api/{self.client.LatestAPIversion}/app/clinical/opendata/{object_name}/{record_id}/affiliations"

        headers = {
            "Accept": accept,
        }

        return self.client.api_call(endpoint=endpoint, method="GET", headers=headers)

    def change_primary_investigator_affiliation(self, data: list) -> Dict[str, Any]:
        """
        Change the Primary Affiliation of an Investigator mapped to OpenData Clinical in bulk.
        This API supports changes to existing OpenData Clinical investigators and requests to
        add new Investigators. Update or Create up to 100 records per request.

        Args:
            data: A list of dictionaries containing the records to update. Maximum 100 records.
                  Each entry must contain:
                  - person_sys: The record ID of the person__sys record whose primary affiliation
                    is being modified.
                  - hco_opendata_id: The hco_link_id of the OpenData Clinical site that will now
                    be used for the primary affiliation. This will be copied onto the contact
                    information of type person_linked_contact_information__v.

        Returns:
            API response containing information about the Person or Organization mapped to
            OpenData Clinical
        """
        endpoint = f"api/{self.client.LatestAPIversion}/app/clinical/opendata/person__sys/primary_affiliations"

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        return self.client.api_call(
            endpoint=endpoint, method="POST", headers=headers, json=data
        )

    def populate_procedure_definitions(self, data: list) -> Dict[str, Any]:
        """
        Use this request to initiate the Populate Procedure Definitions user action.
        This action creates Procedure Definitions for a target study from a source study
        or an existing Procedure Template.

        Learn more about Procedure Definitions in Vault Help.

        Args:
            data: A list containing a dictionary with the following keys:
                source_holder_object_name (required): The name of the object to create Procedure Definitions from
                                                     (study__v or procedure_template__v).
                source_holder_object_ids (required): An array of study or Procedure Template IDs to copy Procedure
                                                    Definitions from.
                destination_holder_object_name (required): The name of the object to create Procedure Definitions for.
                                                         This must always be study__v.
                destination_holder_object_id (required): The ID of the study to populate with Procedure Definitions.

        Returns:
            API response with status and details of the operation
        """
        endpoint = f"api/{self.client.LatestAPIversion}/app/clinical/ctms/populate-procedure-definitions"

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        return self.client.api_call(
            endpoint=endpoint, method="POST", headers=headers, json=data
        )

    def initiate_clinical_record_merge(
        self, object_name: str, data: Union[list, Any]
    ) -> Dict[str, Any]:
        """
        Initiate a record merge operation in bulk to eliminate duplicate Global Directory data
        in your Clinical Operations Vault. When merging two records together, you must select
        one record to be the main_record_id and one record to be the duplicate_record_id.
        The merging process updates all inbound references (including attachments) from other
        objects that point to the duplicate record and moves those over to the main record.
        Field values on the main record are not changed, and when the process is complete,
        the duplicate record is deleted. Record merges do not trigger record triggers.

        You can only merge two records together in a single operation, one main record and
        one duplicate record. This is called a merge set. If you have multiple duplicate
        records you wish to merge into the same main record, you need to create multiple
        merge sets and execute multiple record merges.

        The values in the input must be UTF-8 encoded.
        CSVs must follow the standard RFC 4180 format, with some exceptions.
        The maximum batch size is 10 merge sets.
        The maximum number of concurrent merge requests is 500.

        This request only supports record merges for the following objects:
        - Person (person__sys)
        - Organization (organization__v)
        - Location (location__v)
        - Contact Information (contact_information__clin)

        Each object above must have Enable Merges configured and the initiating user must
        have the Application: Object: Merge Records permission. To merge records for other
        objects in your Vault, use Initiate Record Merge. Learn more about record merges
        for Clinical Operations in Vault Help.

        Args:
            object_name: The name of the object to merge. Possible values are person__sys,
                        organization__v, location__v, and contact_information__clin.
            data: JSON or CSV data containing the merge operations. Upload parameters as a
                  JSON or CSV file. You can merge up to 10 merge sets at once. Each entry
                  must contain:
                  - duplicate_record_id (required): The ID of the duplicate record. Each
                    duplicate_record_id can only be merged into one main_record_id record.
                    When the merging process is complete, Vault deletes this record.
                  - main_record_id (required): The ID of the main record. The merging process
                    updates all inbound references (including attachments) from other objects
                    that point to the duplicate record and moves those over to the main record.
                    Vault does not change field values on the main record.

        Returns:
            API response containing jobID for successful operation
        """
        endpoint = f"api/{self.client.LatestAPIversion}/app/clinical/objects/{object_name}/actions/merge"

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        return self.client.api_call(
            endpoint=endpoint, method="POST", headers=headers, json=data
        )

    def enable_study_migration_mode(self, data: list) -> Dict[str, Any]:
        """
        Enable Study Migration Mode for multiple Study records. Sending a request to this
        endpoint initiates a job to set the study_migration__v field on Study records and
        their related object records with the value m__v. You can enable Study Migration
        Mode for up to 500 Study records in a single request.

        When a Study enters Study Migration Mode, Vault makes study-related object data
        for that study hidden and uneditable for non-Admin users. Study Migration Mode
        also bypasses record triggers for the target studies, such as calculating metrics
        and generating related records. Learn more about status and archiving studies in
        Vault Help. Learn more about Clinical Study Migrations.

        Args:
            data: A list of dictionaries containing Study record IDs:
                  - id (required): The ID of the Study record.

        Returns:
            API response containing jobID and url for successful operation
        """
        endpoint = f"api/{self.client.LatestAPIversion}/app/clinical/studies/actions/enable_migration_mode"

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        return self.client.api_call(
            endpoint=endpoint, method="POST", headers=headers, json=data
        )

    def disable_study_migration_mode(self, data: list) -> Dict[str, Any]:
        """
        Disable Study Migration Mode for multiple Study records. Sending a request to this
        endpoint initiates a job to clear the study_migration__v field on Study records and
        their related object records. You can disable Study Migration Mode for up to 500
        Study records in a single request.

        Learn more about status and archiving studies in Vault Help. Learn more about
        Clinical Study Migrations.

        Args:
            data: A list of dictionaries containing Study record IDs:
                  - id (required): The ID of the Study record.

        Returns:
            API response containing jobID and url for successful operation
        """
        endpoint = f"api/{self.client.LatestAPIversion}/app/clinical/studies/actions/disable_migration_mode"

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        return self.client.api_call(
            endpoint=endpoint, method="POST", headers=headers, json=data
        )

    def retrieve_opendata_clinical_affiliations(
        self, object_name: str, record_id: str, accept: str = "application/json"
    ) -> Dict[str, Any]:
        """
        Given a Person or Organization mapped to OpenData Clinical, retrieves contact
        information associated with the Investigator Site record.

        This API returns a maximum of 100 records. If there are more than 100 records to
        return, Vault truncates records beyond 100 in the returned response. To retrieve
        more than 100 records, use Direct Data API.

        Args:
            object_name: The name of the object to merge. Possible values are person__sys,
                        organization__v, location__v, and contact_information__clin.
            record_id: The ID of the person__sys or organization__v record.
            accept: Accepted response format (default: "application/json"). Can also be "text/csv".

        Returns:
            API response containing information about the Person or Organization mapped to
            OpenData Clinical
        """
        endpoint = f"api/{self.client.LatestAPIversion}/app/clinical/opendata/{object_name}/{record_id}/affiliations"

        headers = {
            "Accept": accept,
        }

        return self.client.api_call(endpoint=endpoint, method="GET", headers=headers)

    def change_primary_investigator_affiliation(self, data: list) -> Dict[str, Any]:
        """
        Change the Primary Affiliation of an Investigator mapped to OpenData Clinical in bulk.
        This API supports changes to existing OpenData Clinical investigators and requests to
        add new Investigators. Update or Create up to 100 records per request.

        Args:
            data: A list of dictionaries containing the records to update. Maximum 100 records.
                  Each entry must contain:
                  - person_sys: The record ID of the person__sys record whose primary affiliation
                    is being modified.
                  - hco_opendata_id: The hco_link_id of the OpenData Clinical site that will now
                    be used for the primary affiliation. This will be copied onto the contact
                    information of type person_linked_contact_information__v.

        Returns:
            API response containing information about the Person or Organization mapped to
            OpenData Clinical
        """
        endpoint = f"api/{self.client.LatestAPIversion}/app/clinical/opendata/person__sys/primary_affiliations"

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        return self.client.api_call(
            endpoint=endpoint, method="POST", headers=headers, json=data
        )
