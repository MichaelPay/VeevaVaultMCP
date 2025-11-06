class VaultJavaSdkService:
    """
    Service class for managing Vault Java SDK code.

    This service provides methods to interact with all Java SDK-related API endpoints,
    allowing retrieval, enabling/disabling, adding/replacing, and deleting source code files,
    as well as managing packages and certificates.
    """

    def __init__(self, client):
        """
        Initialize with a VaultClient instance

        Args:
            client: An initialized VaultClient instance for API communication
        """
        self.client = client

    def retrieve_source_code_file(self, class_name):
        """
        Retrieves a single source code file from the currently authenticated Vault.

        Corresponds to GET /api/{version}/code/{class_name}

        Args:
            class_name (str): The fully qualified class name of your file.

        Returns:
            str: The source code content of the requested Java file.
        """
        url = f"api/{self.client.LatestAPIversion}/code/{class_name}"
        return self.client.api_call(url, return_raw=True)

    def enable_vault_extension(self, class_name):
        """
        Enables a deployed Vault extension in the currently authenticated Vault.

        Corresponds to PUT /api/{version}/code/{class_name}/enable

        Only available on entry-point classes, such as triggers and actions.

        Args:
            class_name (str): The fully qualified class name of your file.

        Returns:
            dict: The JSON response containing:
                - responseStatus: "SUCCESS" if successful
                - responseMessage: Confirmation message (e.g., "Enabled")
        """
        url = f"api/{self.client.LatestAPIversion}/code/{class_name}/enable"
        return self.client.api_call(url, method="PUT")

    def disable_vault_extension(self, class_name):
        """
        Disables a deployed Vault extension in the currently authenticated Vault.

        Corresponds to PUT /api/{version}/code/{class_name}/disable

        Only available on entry-point classes, such as triggers and actions.

        Args:
            class_name (str): The fully qualified class name of your file.

        Returns:
            dict: The JSON response containing:
                - responseStatus: "SUCCESS" if successful
                - responseMessage: Confirmation message (e.g., "Disabled")
        """
        url = f"api/{self.client.LatestAPIversion}/code/{class_name}/disable"
        return self.client.api_call(url, method="PUT")

    def add_or_replace_source_code_file(self, file_path):
        """
        Adds or replaces a single .java file in the currently authenticated Vault.

        Corresponds to PUT /api/{version}/code

        If the given file does not already exist in the Vault, it is added.
        If the file already exists in the Vault, the file is updated.

        Note:
            We do not recommend using this method to deploy code as you may introduce code
            which breaks existing deployed code. For best practices, use the VPK Deploy method.

        Args:
            file_path (str): Path to the .java file you wish to add or replace.

        Returns:
            dict: The JSON response containing:
                - responseStatus: "SUCCESS" if successful
                - responseMessage: Confirmation message (e.g., "Modified file")
                - url: The URL to retrieve the updated file

        Notes:
            Maximum allowed file size is 1MB.
        """
        url = f"api/{self.client.LatestAPIversion}/code"
        files = {"file": open(file_path, "rb")}
        return self.client.api_call(url, method="PUT", files=files)

    def delete_source_code_file(self, class_name):
        """
        Deletes a single source code file from the currently authenticated Vault.

        Corresponds to DELETE /api/{version}/code/{class_name}

        Note:
            We do not recommend using this method to deploy code as you may delete code
            which breaks existing deployed code. For best practices, use the VPK Deploy method.
            You cannot delete a code component currently in-use.

        Args:
            class_name (str): The fully qualified class name of your file.

        Returns:
            dict: The JSON response containing:
                - responseStatus: "SUCCESS" if successful
                - responseMessage: Confirmation message (e.g., "Deleted file")
        """
        url = f"api/{self.client.LatestAPIversion}/code/{class_name}"
        return self.client.api_call(url, method="DELETE")

    def validate_imported_package(self, package_id):
        """
        Validates a previously imported VPK package with Vault Java SDK code.

        Corresponds to POST /api/{version}/services/vobject/vault_package__v/{package_id}/actions/validate

        Note:
            This endpoint does not validate component dependencies for Configuration Migration packages.

        Args:
            package_id (str): The ID of the package to validate. You can find this in the API response
                             of a package import, or in the URL of package in the Vault UI.

        Returns:
            dict: The JSON response containing detailed package validation information including:
                - summary: Package description
                - author: Package creator's email
                - package_name: Package name
                - package_id: Package ID
                - source_vault: Source Vault ID
                - package_status: Status (e.g., "Error", "Success")
                - total_steps: Total validation steps
                - start_time: Validation start time
                - end_time: Validation end time
                - package_error: Any package-level errors
                - package_steps: Detailed information about each component validated
        """
        url = f"api/{self.client.LatestAPIversion}/services/vobject/vault_package__v/{package_id}/actions/validate"
        return self.client.api_call(url, method="POST")

    def retrieve_signing_certificate(self, cert_id):
        """
        Retrieves a signing certificate included in a Spark message header.

        Corresponds to GET /api/{version}/services/certificate/{cert_id}

        Use this endpoint to verify that a received Spark message came from Vault.

        Args:
            cert_id (str): The certificate ID provided in each Spark message
                          in the X-VaultAPISignature-CertificateId header.

        Returns:
            str: The public key certificate (.pem) file used for Message Verification.
        """
        url = f"api/{self.client.LatestAPIversion}/services/certificate/{cert_id}"
        return self.client.api_call(url, return_raw=True)

    def retrieve_all_queues(self):
        """
        Retrieves all queues in a Vault.

        Corresponds to GET /api/{version}/services/queues

        The current user must have the relevant Admin: Spark Queues or Admin: SDK Job Queues
        permissions to see each queue type. For example, if the API user does not have access
        to SDK job queues, this method only returns available Spark messaging queues.

        Returns:
            dict: The JSON response containing:
                - responseStatus: "SUCCESS" if successful
                - data: A list of queues, each with:
                    - name: Queue name
                    - status: Operational status (e.g., "active")
                    - type: Queue type (e.g., "inbound", "outbound")
                    - url: URL to retrieve detailed queue status
        """
        url = f"api/{self.client.LatestAPIversion}/services/queues"
        return self.client.api_call(url)

    def retrieve_queue_status(self, queue_name):
        """
        Retrieves the status of a specific queue.

        Corresponds to GET /api/{version}/services/queues/{queue_name}

        Args:
            queue_name (str): The name of a specific queue. For example, queue__c.

        Returns:
            dict: The JSON response containing detailed queue status information:
                - name: Queue name
                - status: Operational status (e.g., "active")
                - type: Queue type (e.g., "outbound")
                - delivery: Delivery status (e.g., "enabled")
                - messages_in_queue: Number of messages in the queue
                - connections: List of connection details, each with:
                    - name: Connection name
                    - last_message_delivered: Delivery status (e.g., "error", "ok")
                    - error: (if applicable) Error details including message_id, date_time, and message
        """
        url = f"api/{self.client.LatestAPIversion}/services/queues/{queue_name}"
        return self.client.api_call(url)

    def disable_queue_delivery(self, queue_name):
        """
        Disables the delivery of messages in a queue.

        Corresponds to PUT /api/{version}/services/queues/{queue_name}/actions/disable_delivery

        This stops messages from exiting the queue. For example, disabling delivery on an SDK job
        queue stops messages from being delivered to the processor.

        Note:
            This endpoint is not available for inbound Spark messaging queues. There is no way
            to stop received messages from processing in an inbound Spark queue.

        Args:
            queue_name (str): The name of a specific queue.

        Returns:
            dict: The JSON response containing:
                - responseStatus: "SUCCESS" if successful
        """
        url = f"api/{self.client.LatestAPIversion}/services/queues/{queue_name}/actions/disable_delivery"
        return self.client.api_call(url, method="PUT")

    def enable_queue_delivery(self, queue_name):
        """
        Enables the delivery of messages in a queue.

        Corresponds to PUT /api/{version}/services/queues/{queue_name}/actions/enable_delivery

        This allows messages to exit the queue. For example, enabling delivery on an SDK job
        queue allows messages to be delivered to the processor.

        Args:
            queue_name (str): The name of a specific queue.

        Returns:
            dict: The JSON response containing:
                - responseStatus: "SUCCESS" if successful
        """
        url = f"api/{self.client.LatestAPIversion}/services/queues/{queue_name}/actions/enable_delivery"
        return self.client.api_call(url, method="PUT")

    def reset_queue(self, queue_name):
        """
        Deletes all messages in a specific queue.

        Corresponds to PUT /api/{version}/services/queues/{queue_name}/actions/reset

        This action is final and cannot be undone.

        Args:
            queue_name (str): The name of a specific queue.

        Returns:
            dict: The JSON response containing:
                - responseStatus: "SUCCESS" if successful
                - responseMessage: Confirmation message (e.g., "Deleted messages in queue.")
        """
        url = f"api/{self.client.LatestAPIversion}/services/queues/{queue_name}/actions/reset"
        return self.client.api_call(url, method="PUT")
