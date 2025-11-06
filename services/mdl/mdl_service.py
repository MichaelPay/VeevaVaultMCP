import requests
import os


class MDLService:
    """
    Service class for handling Metadata Definition Language (MDL) operations with Veeva Vault.
    MDL is used to create, describe (read), update, and drop (delete) Vault components and manage its configuration.
    """

    def __init__(self, client):
        """
        Initialize with a VaultClient instance

        :param client: An initialized VaultClient instance with valid sessionId and vaultURL
        """
        self.client = client

    def execute_mdl_script(self, mdl_script):
        """
        Executes the given MDL script on a Vault synchronously.

        This endpoint executes the given MDL script on a Vault. Note that some large operations
        require use of the asynchronous endpoint. The body of the request should contain
        the MDL script to execute as raw data, starting with one of the following values:
        CREATE, RECREATE, RENAME, ALTER, DROP.

        Args:
            mdl_script (str): The MDL script to be executed as a raw string.

        Returns:
            dict: On SUCCESS, the response contains details of the execute, including:
                - responseStatus: Status of the response
                - script_execution: Contains execution details including code, message, warnings,
                  failures, exceptions, components_affected, and execution_time
                - statement_execution: List of execution details for each statement
        """
        url = f"{self.client.vaultURL}/api/mdl/execute"

        headers = {
            "Authorization": self.client.sessionId,
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        response = requests.post(url, headers=headers, data=mdl_script)
        return response.json()

    def execute_mdl_script_async(self, mdl_script):
        """
        Executes the given MDL script on a Vault asynchronously.

        This asynchronous endpoint executes the given MDL script on a Vault.
        While you can execute any MDL script with this endpoint, it is required if you're operating
        on 10,000+ raw object records and executing operations like:
        - Enabling lifecycles
        - Enabling or disabling object types
        - Adding or removing a field
        - Updating the max length of any variable-length field
        - Adding or removing an Index
        - Changing the fields that compose an Index

        After initiating this request, your raw object's configuration_state becomes IN_DEPLOYMENT.
        This endpoint can only queue one asynchronous change at a time.

        Args:
            mdl_script (str): The MDL script to be executed as a raw string, starting with one of
                             the valid MDL commands (CREATE, RECREATE, RENAME, ALTER, DROP).

        Returns:
            dict: On SUCCESS, the response includes:
                - responseStatus: Status of the response
                - script_execution: Contains execution details
                - job_id: The Job ID value to retrieve the status and results of this request
                - url: URL to retrieve the current job status of this request
        """
        url = f"{self.client.vaultURL}/api/mdl/execute_async"

        headers = {
            "Authorization": self.client.sessionId,
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        response = requests.post(url, headers=headers, data=mdl_script)
        return response.json()

    def retrieve_async_mdl_script_results(self, job_id):
        """
        Retrieves the results of an asynchronously executed MDL script.

        After submitting a request to deploy an MDL script asynchronously, you can query
        Vault to determine the results of the request.

        Before submitting this request:
        - You must have previously requested a submission export job (via the API) which is no longer active.
        - You must have a valid job_id field value returned from the Execute MDL Script Asynchronously request.

        Args:
            job_id (int): The job_id field value that was returned from the Execute MDL
                         Script Asynchronously request.

        Returns:
            dict: On SUCCESS, this endpoint returns the results of the asynchronous MDL script
                 execution, including any errors, with details like:
                - responseStatus: Status of the response
                - script_execution: Contains execution details
                - statement_execution: List of execution details for each statement
        """
        url = f"{self.client.vaultURL}/api/mdl/execute_async/{job_id}/results"

        headers = {"Authorization": self.client.sessionId, "Accept": "application/json"}

        response = requests.get(url, headers=headers)
        return response.json()

    def cancel_raw_object_deployment(self, object_name):
        """
        Cancels a deployment of configuration changes to a raw object.

        To use this endpoint, your raw object configuration_state must be IN_DEPLOYMENT.

        Args:
            object_name (str): The name of the object on which to cancel deployment.
                              This object's configuration_state must be IN_DEPLOYMENT.

        Returns:
            dict: If the deployment is cancelled successfully, the API returns SUCCESS.
        """
        url = f"{self.client.vaultURL}/api/{self.client.LatestAPIversion}/metadata/vobjects/{object_name}/actions/canceldeployment"

        headers = {"Authorization": self.client.sessionId, "Accept": "application/json"}

        response = requests.post(url, headers=headers)
        return response.json()

    def retrieve_all_component_metadata(self):
        """
        Retrieves metadata of all component types in your Vault.

        This endpoint provides information about all available component types that can be
        managed through MDL in the Vault.

        Returns:
            dict: On SUCCESS, the response may include the following for each component type:
                - url: URL to retrieve metadata for the component type
                - name: The component type name as used in MDL commands
                - class: The class of the component type (code or metadata)
                - abbreviation: The abbreviated component type name
                - label: The component type label as it appears in the Vault UI
                - label_plural: The plural component type label as it appears in the Vault UI
                - cacheable: Indicates whether the component type has a cache
                - cache_type_class: Indicates the caching strategy used by the component type
                - vobject: The associated Vault object, if applicable
        """
        url = f"{self.client.vaultURL}/api/{self.client.LatestAPIversion}/metadata/components"

        headers = {"Authorization": self.client.sessionId, "Accept": "application/json"}

        response = requests.get(url, headers=headers)
        return response.json()

    def retrieve_component_type_metadata(self, component_type):
        """
        Retrieves metadata of a specific component type.

        This endpoint provides detailed information about a specific component type,
        including its attributes and sub-components.

        Args:
            component_type (str): The component type name (Picklist, Docfield, Doctype, etc.).

        Returns:
            dict: On SUCCESS, the response contains metadata for the specified component type.
                 Metadata returned varies for each component and subcomponent type, including:
                - name: Component type name
                - class: Component type class (metadata or code)
                - abbreviation: Abbreviated name
                - active: Whether the component type is active
                - attributes: List of attributes for the component type
                - sub_components: List of sub-components, if applicable
        """
        url = f"{self.client.vaultURL}/api/{self.client.LatestAPIversion}/metadata/components/{component_type}"

        headers = {"Authorization": self.client.sessionId, "Accept": "application/json"}

        response = requests.get(url, headers=headers)
        return response.json()

    def retrieve_component_record_collection(self, component_type):
        """
        Retrieves all records for a specific component type.

        This endpoint does not support retrieving Object component records. Instead,
        use Retrieve Object Collection.

        Args:
            component_type (str): The component type name (Picklist, Docfield, Doctype, etc.).
                                 To retrieve records for Object, see Retrieve Object Collection.

        Returns:
            dict: On SUCCESS, the response contains all component records in the Vault for
                 the specified component type. Each component record returns a minimum of
                 API name and UI label, but most types return more.
        """
        url = f"{self.client.vaultURL}/api/{self.client.LatestAPIversion}/configuration/{component_type}"

        headers = {"Authorization": self.client.sessionId, "Accept": "application/json"}

        response = requests.get(url, headers=headers)
        return response.json()

    def retrieve_component_record(self, component_type_and_record_name, loc=False):
        """
        Retrieves metadata of a specific component record as JSON or XML.

        Not all component types are eligible for record description retrieval.

        Args:
            component_type_and_record_name (str): The component type name followed by the name
                                               of the record from which to retrieve metadata.
                                               The format is {Componenttype}.{record_name}.
                                               For example, Picklist.color__c.
            loc (bool, optional): When localized (translated) strings are available,
                                 retrieve them by setting loc to true. Defaults to False.

        Returns:
            dict: On SUCCESS, the response contains the complete definition for a specific
                 component record. If a field returns as blank or null, it means the record
                 has no value for that field.
        """
        url = f"{self.client.vaultURL}/api/{self.client.LatestAPIversion}/configuration/{component_type_and_record_name}"

        if loc:
            url += "?loc=true"

        headers = {"Authorization": self.client.sessionId, "Accept": "application/json"}

        response = requests.get(url, headers=headers)
        return response.json()

    def retrieve_component_record_mdl(self, component_type_and_record_name):
        """
        Retrieves metadata of a specific component record as MDL.

        Vault does not generate RECREATE statements for all component types.

        Args:
            component_type_and_record_name (str): The component type name followed by the name
                                               of the record from which to retrieve metadata.
                                               The format is {Componenttype}.{record_name}.
                                               For example, Picklist.color__c.

        Returns:
            str: On SUCCESS, the response contains a RECREATE MDL statement of metadata for
                the specified component record. Metadata returned varies based on component type.
                If a field returns as blank, it means the record currently has no value for that field.
        """
        url = f"{self.client.vaultURL}/api/mdl/components/{component_type_and_record_name}"

        headers = {"Authorization": self.client.sessionId, "Accept": "application/json"}

        response = requests.get(url, headers=headers)
        return response.text

    def upload_content_file(self, file_path):
        """
        Uploads a content file to be referenced by a component.

        Once uploaded, Vault stores the file in a generic files staging area where they will
        remain until referenced by a component. Once referenced, Vault cannot access the
        named file from the staging area.

        Args:
            file_path (str): The local file path of the content file to be uploaded.
                           For example, 'C:\\Quote.pdf'.

        Returns:
            dict: On SUCCESS, the response includes the following:
                - name__v: The name of the file which can be used in MDL for referencing the component
                - format__v: The format of the file
                - size__v: The file size of the file
                - sha1_checksum__v: The SHA-1 checksum value generated for the file
        """
        url = f"{self.client.vaultURL}/api/mdl/files"

        headers = {
            "Authorization": self.client.sessionId,
            "Accept": "application/json",
        }

        with open(file_path, "rb") as file:
            files = {"file": (os.path.basename(file_path), file)}
            response = requests.post(url, headers=headers, files=files)

        return response.json()

    def retrieve_content_file(self, component_type_and_record_name):
        """
        Retrieves the content file metadata of a specified component.

        This endpoint retrieves information about content files associated with components
        that contain binary content as part of their definition, such as Formattedoutput,
        Overlaytemplate, and Signaturepage.

        Args:
            component_type_and_record_name (str): The component type of the record followed by
                                               the name of the record from which to retrieve
                                               the content file. The format is
                                               {Componenttype}.{record_name}.
                                               For example, 'Formattedoutput.my_formatted_output__c'.

        Returns:
            dict: On SUCCESS, the response includes the following:
                - links: Contains rel, href, method, and accept for accessing the actual file
                - data: Information about the file including:
                  - name__v: The name of the file which can be used in MDL for referencing the component
                  - original_name__v: The original name of the uploaded file
                  - format__v: The format of the file
                  - size__v: The file size of the file
                  - sha1_checksum__v: The SHA-1 checksum value generated for the file
        """
        url = f"{self.client.vaultURL}/api/mdl/components/{component_type_and_record_name}/files"

        headers = {"Authorization": self.client.sessionId, "Accept": "application/json"}

        response = requests.get(url, headers=headers)
        return response.json()
