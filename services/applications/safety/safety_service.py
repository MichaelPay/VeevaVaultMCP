from typing import Dict, Any, Optional, Union, BinaryIO
import json


class SafetyService:
    """
    Service class for interacting with the Veeva Vault Safety application.

    This service provides methods for working with Inbox items, case imports, and narratives.
    """

    def __init__(self, client):
        """
        Initialize the SafetyService with a VaultClient instance.

        Args:
            client: An initialized VaultClient instance for API communication
        """
        self.client = client

    def intake_inbox_item(
        self,
        file_path: str,
        format: str,
        origin_organization: Optional[str] = None,
        organization: Optional[str] = None,
        transmission_profile: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Import an Inbox Item from an E2B (R2) or E2B (R3) file containing one or more Individual Case Safety Reports (ICSRs).

        Args:
            file_path: The filepath of the E2B file to be imported.
            format: The format of the file being imported. This must match the Vault API Name
                  of the Inbound Transmission Format picklist value. Must be an E2B format.
            origin_organization: (Optional) The Vault API Name for the Organization sending the E2B file.
                                This parameter sets the Origin Organization on the Inbound Transmission.
                                If no value is provided, the Origin Organization is left blank.
            organization: (Optional) To specify which organization to send the Case to, enter the
                        Vault API Name for the Organization record. If no value is provided, the
                        Organization is set to vault_customer__v. Note that the Organization record
                        type must be Sponsor.
            transmission_profile: (Optional) The Vault API Name of the Transmission Profile to be used
                                 for E2B Intake. These parameters are used for Narrative Template Override
                                 and Inbox Item Auto-Promotion. The Transmission Profile record type must
                                 be Connection. This parameter is required for Automated Case Promotion.
                                 If no transmission-profile is specified, Vault will use the parameters
                                 on the general_api_profile__v.

        Returns:
            API response containing the URL to check the status and the intake_id
        """
        endpoint = f"api/{self.client.LatestAPIversion}/app/safety/intake/inbox-item"

        files = {"file": open(file_path, "rb")}
        data = {"format": format}

        if origin_organization:
            data["origin-organization"] = origin_organization
        if organization:
            data["organization"] = organization
        if transmission_profile:
            data["transmission-profile"] = transmission_profile

        return self.client.api_call(
            endpoint=endpoint, method="POST", files=files, data=data
        )

    def intake_imported_case(
        self,
        file_path: str,
        format: str,
        organization: Optional[str] = None,
        origin_organization: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Import an Imported Case from an E2B (R2) or E2B (R3) file containing one or more Individual Case Safety Reports (ICSRs).

        Args:
            file_path: The filepath of the E2B file to be imported.
            format: The format of the file being imported. This must match the Vault API Name
                  of the Inbound Transmission Format picklist value. Must be an E2B format or other__v.
                  If other__v, the system does not attempt E2B import or forms processing and instead
                  creates an empty Inbox Item linked to the source document.
            organization: (Optional) To specify which organization to send the Case to, enter the
                        Vault API Name for the Organization record. If no value is provided, the
                        Organization is set to vault_customer__v. Note that the Organization record
                        type must be Sponsor.
            origin_organization: (Optional) The Vault API Name for the Organization sending the E2B file.
                                This parameter sets the Origin Organization on the Inbound Transmission.
                                If no value is provided, the Origin Organization is left blank.

        Returns:
            API response containing the URL to check the status of the import request and the intake ID of the E2B import.
        """
        endpoint = f"api/{self.client.LatestAPIversion}/app/safety/intake/imported-case"

        files = {"file": open(file_path, "rb")}
        data = {"format": format}

        if organization:
            data["organization"] = organization
        if origin_organization:
            data["origin-organization"] = origin_organization

        return self.client.api_call(
            endpoint=endpoint, method="POST", files=files, data=data
        )

    def retrieve_intake_status(self, inbound_id: str) -> Dict[str, Any]:
        """
        Retrieve the status of an intake API call.

        The Retrieve Intake Status endpoint can be used with the following Safety intake endpoints:
        - Intake Inbox Item
        - Intake Imported Case

        Args:
            inbound_id: The Inbound Transmission ID for the ICSR intake job.

        Returns:
            API response containing details about the status of the intake job including:
            - status: Processing status for the intake job.
            - ack-retrieval: URL to retrieve the ACK. This parameter only applies to E2B intake file types.
            - inbound-transmission: ID or link to the Inbound Transmission for the entire intake job.
            - inbound-document: ID or link to the Vault document created from E2B file for the entire intake job.
            - number-cases: Total number of cases found in the intake file, including both successes and failures.
            - number-successes: Number of cases that were imported successfully, including those with warnings.
            - number-failures: Number of cases that failed to import.
            - icsr-details: An array containing details for each individual case within the file.
        """
        endpoint = f"api/{self.client.LatestAPIversion}/app/safety/intake/status"

        params = {"inbound_id": inbound_id}

        headers = {"Accept": "application/json"}

        return self.client.api_call(
            endpoint=endpoint, method="GET", headers=headers, params=params
        )

    def retrieve_ack(self, inbound_id: str) -> Dict[str, Any]:
        """
        Retrieve the E2B acknowledgement message (ACK) after sending an intake call.

        The Retrieve ACK endpoint can be used with the following Safety intake endpoints:
        - Intake Inbox Item
        - Intake Imported Case

        Args:
            inbound_id: The Inbound Transmission ID for the ICSR intake job.

        Returns:
            The ACK XML. The ACK is returned in the same E2B format as the intake file.
        """
        endpoint = f"api/{self.client.LatestAPIversion}/app/safety/intake/ack"

        params = {"inbound_id": inbound_id}

        headers = {"Accept": "application/json"}

        return self.client.api_call(
            endpoint=endpoint,
            method="GET",
            headers=headers,
            params=params,
            raw_response=True,
        )

    def intake_json(
        self,
        api_name: str,
        intake_json: Union[str, BinaryIO],
        intake_form: Optional[Union[str, BinaryIO]] = None,
    ) -> Dict[str, Any]:
        """
        Use this endpoint to send JSON to Veeva Safety, which will be imported to a single Inbox Item.

        Before submitting this request:
        - The User record for the API user must link to the Organization receiving the report in the
          Organization field. Edit User records in Admin > Users & Groups.
        - The API user must have the Access API Vault Action permission in their permission set.

        Args:
            api_name: (Optional) To specify which organization to send the Inbox Item to, enter the Vault
                     API Name for the Organization record. The default value is vault_customer.
                     Note that the Organization record type must be Sponsor.
            intake_json: The filepath for the JSON intake file, or the raw JSON text. Veeva Safety
                        creates an Inbox Item using the JSON passed through this parameter.
                        Note that Veeva Safety does not support bulk intake with this endpoint.
                        A single API call is required for each Inbox Item. Ensure to use the correct JSON format.
            intake_form: The filepath for a source intake document. Veeva Safety attaches the file passed
                        through intake_form to the Inbox Item and Inbound Transmission.

        Returns:
            API response containing the jobID, which you can use to retrieve the job status,
            and the transmissionRecordId, which you can use to find the Inbound Transmission
            record in your Vault.
        """
        endpoint = f"api/{self.client.LatestAPIversion}/app/safety/ai/intake?API_Name={api_name}"

        files = {}
        if isinstance(intake_json, str) and (
            intake_json.endswith(".json")
            or intake_json.startswith("{")
            or intake_json.startswith("[")
        ):
            # If it's a file path or raw JSON
            if intake_json.endswith(".json"):
                files["intake_json"] = open(intake_json, "rb")
            else:
                files["intake_json"] = intake_json
        else:
            # If it's already a file-like object
            files["intake_json"] = intake_json

        if intake_form:
            if isinstance(intake_form, str):
                files["intake_form"] = open(intake_form, "rb")
            else:
                files["intake_form"] = intake_form

        content_type = "multipart/form-data" if intake_form else "application/json"

        headers = {
            "Content-Type": content_type,
        }

        return self.client.api_call(
            endpoint=endpoint, method="POST", headers=headers, files=files
        )

    def import_narrative(
        self,
        case_id: str,
        narrative_type: str,
        narrative_language: str,
        narrative_text: str,
        link_translation_to_primary: bool = False,
    ) -> Dict[str, Any]:
        """
        Use this endpoint to import narrative text into a Case narrative.

        The request creates a narrative document for the destination Case, in the format of the
        E2B import narrative template. The narrative text sent in the body of this call is
        appended to the template content.

        If a Case narrative document already exists for the given language, the request creates
        a new version of the document and appends the narrative text sent in the body of this
        call to the existing content.

        Before submitting this request:
        - You must be assigned permissions to use the API and have the Edit Document permission
          for the draft__v state of the narrative_lifecycle__v object.
        - The destination Case must exist.

        Args:
            case_id: Destination Case or Adverse Event Report ID.
            narrative_type: For the main narrative, enter primary. For a narrative translation, enter translation.
                          The primary narrative must exist before you can add a translation.
            narrative_language: Three-letter ISO 639-2 language code.
                              Currently, the primary narrative must be English (eng).
            narrative_text: The narrative text content. You can import up to 100,000 characters of narrative text.
            link_translation_to_primary: Set to true to add the localized narrative document as a supporting document
                                       to the global (English) narrative document. This parameter only applies
                                       when the narrativeType is set to translation and the localized
                                       narrative document does not already exist. If omitted, defaults to false.

        Returns:
            API response with status of the request
        """
        endpoint = f"api/{self.client.LatestAPIversion}/app/safety/import-narrative"

        headers = {
            "Content-Type": "text/plain",
            "caseId": case_id,
            "narrativeType": narrative_type,
            "narrativeLanguage": narrative_language,
        }

        if link_translation_to_primary:
            headers["link_translation_to_primary"] = "true"

        return self.client.api_call(
            endpoint=endpoint, method="POST", headers=headers, data=narrative_text
        )

    def bulk_import_narrative(
        self,
        narratives_file: Union[str, BinaryIO],
        integrity_check: bool = False,
        migration_mode: bool = False,
        archive_document: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """
        Use this endpoint to bulk import case narratives into Veeva Safety.

        This request imports text to create multiple narrative documents, in the format of the
        E2B import narrative template. This request can import primary narratives as well as
        narrative translations. Narrative translations can optionally be imported to a Localized
        Case in addition to the global Case.

        If a Case narrative or translation already exists for the given language, the request creates
        a new version of the document populated with the text sent through the request.

        This endpoint is asynchronous. The following limits apply to this endpoint:
        - The maximum batch size is 500
        - The maximum CSV input file size is 100 MB
        - Maximum characters per narrative is 200k
        - The CSV file cannot contain duplicate rows with the same caseId and narrativeLanguage
        - As this endpoint is asynchronous, multiple Bulk Import Narrative requests cannot run at the same time.
          Use the Retrieve Bulk Import Status endpoint to verify that a Bulk Narrative Import operation
          is complete before sending an additional request.

        Args:
            narratives_file: The CSV file containing the narratives to be imported. Either file path or file-like object.
            integrity_check: Optional: Set to true to perform additional integrity checks on the CSV file.
                          If omitted, defaults to false.
            migration_mode: Optional: Set to true to perform additional verifications on the localizedCaseId,
                          including checking that the caseId refers to the related global Case and
                          the narrativeLanguage matches the language on the Localized Case. If omitted,
                          defaults to false.
            archive_document: Optional: If the Vault Document Archive feature is enabled, set to true to
                           send the imported narrative documents directly to the document archive, or
                           false to create the imported documents as active narratives. If omitted and
                           the Vault Document Archive feature is enabled, the imported narrative documents
                           are sent directly to the document archive.

        Returns:
            API response containing the import_id which can be used to check the status of the operation with
            the Retrieve Bulk Import Status endpoint.
        """
        endpoint = (
            f"api/{self.client.LatestAPIversion}/app/safety/import-narrative/batch"
        )

        headers = {
            "Content-Type": "multipart/form-data",
            "Accept": "text/csv",
        }

        if integrity_check:
            headers["X-VaultAPI-IntegrityCheck"] = "true"
        if migration_mode:
            headers["X-VaultAPI-MigrationMode"] = "true"
        if archive_document is not None:
            headers["X-VaultAPI-ArchiveDocument"] = str(archive_document).lower()

        # Prepare file
        if isinstance(narratives_file, str):
            files = {"narratives": open(narratives_file, "rb")}
        else:
            files = {"narratives": narratives_file}

        return self.client.api_call(
            endpoint=endpoint, method="POST", headers=headers, files=files
        )

    def retrieve_bulk_import_status(self, import_id: str) -> Dict[str, Any]:
        """
        Use this endpoint to retrieve the status of a bulk narrative import.

        Args:
            import_id: The import_id of the bulk narrative import job, retrieved from the job request response details.

        Returns:
            If a bulk import job is complete, the response returns details of each narrative document.
            If a bulk import job is incomplete, the response returns details of the job in progress.
        """
        endpoint = f"api/{self.client.LatestAPIversion}/app/safety/import-narrative/batch/{import_id}"

        headers = {"Accept": "application/json"}

        return self.client.api_call(endpoint=endpoint, method="GET", headers=headers)
