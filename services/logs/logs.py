# logs_service.py
import pandas as pd
import asyncio
import requests
from typing import Dict, List, Optional, Union, Any


class LogsService:
    """
    Service class for managing logs in Veeva Vault.

    This service provides methods to interact with audit trail APIs, audit history APIs,
    debug logs, SDK request profiler, and email notification histories in Veeva Vault.
    """

    def __init__(self, client):
        """
        Initialize with a VaultClient instance

        Args:
            client: An initialized VaultClient instance for API communication
        """
        self.client = client

    def retrieve_audit_types(self):
        """
        Retrieves all audit types you have permission to access.

        Corresponds to GET /api/{version}/metadata/audittrail

        On SUCCESS, returns all available audit types you have permission to access.

        Returns:
            dict: The JSON response containing all audit types with fields:
                - name: Name of the audit type
                - label: Label of the audit type as seen in the API and UI
                - url: URL to retrieve the metadata associated with the audit type
        """
        url = f"api/{self.client.LatestAPIversion}/metadata/audittrail"
        return self.client.api_call(url)

    def retrieve_audit_metadata(self, audit_trail_type: str):
        """
        Retrieves all fields and their metadata for a specified audit trail or log type.

        Corresponds to GET /api/{version}/metadata/audittrail/{audit_trail_type}

        Args:
            audit_trail_type (str): The name of the specified audit type
                (document_audit_trail, object_audit_trail, etc).

        Returns:
            dict: The JSON response containing metadata for the audit type:
                - name: The name of the audit type
                - label: The label of the audit type
                - fields: List of field metadata with name, label, and type
        """
        url = (
            f"api/{self.client.LatestAPIversion}/metadata/audittrail/{audit_trail_type}"
        )
        return self.client.api_call(url)

    def retrieve_audit_details(
        self,
        audit_trail_type: str,
        start_date: str = None,
        end_date: str = None,
        all_dates: bool = False,
        format_result: str = None,
        limit: int = 200,
        offset: int = 0,
        objects: str = None,
        events: str = None,
    ):
        """
        Retrieves all audit details for a specific audit type.

        Corresponds to GET /api/{version}/audittrail/{audit_trail_type}

        This request supports optional parameters to narrow the results to a specified date
        and time within the past 30 days. You can run a full audit export with the same
        formatting as exports you initiate in the UI once per day per audit type by setting
        all_dates to true, leaving start_date and end_date blank, and setting format_result to csv.

        Audit logs support a precision to one second. Events occurring within a single second
        may appear in an unexpected order.

        Args:
            audit_trail_type (str): The name of the specified audit type
                (document_audit_trail, object_audit_trail, etc).
            start_date (str, optional): Specify a start date to retrieve audit information.
                This date cannot be more than 30 days ago. Dates must be YYYY-MM-DDTHH:MM:SSZ format,
                e.g., 2016-01-15T07:00:00Z. If omitted, defaults to the start of the previous day.
            end_date (str, optional): Specify an end date to retrieve audit information.
                This date cannot be more than 30 days ago. Dates must be YYYY-MM-DDTHH:MM:SSZ format,
                e.g., 2016-01-15T07:00:00Z. If omitted, defaults to the current date and time.
            all_dates (bool, optional): Set to true to request audit information for all dates.
                You must leave start_date and end_date blank when requesting an export of a full audit trail.
                You can only run a full audit export (all_dates = true) on each audit type once every 24 hours.
            format_result (str, optional): To request a downloadable CSV file of your audit details, use 'csv'.
                The response contains a jobId to retrieve the job status, which contains a link to download the CSV file.
                If omitted, the API returns a JSON response and does not start a job.
                If all_dates is true, this parameter is required.
            limit (int, optional): Paginate the results by specifying the maximum number of histories per page in the response.
                This can be any value between 1 and 1000. If omitted, defaults to 200.
            offset (int, optional): Paginate the results displayed per page by specifying the amount of offset.
                For example, if you are viewing the first 50 results (page 1) and want to see the next page,
                set this to offset=51. If omitted, defaults to 0.
            objects (str, optional): This is an optional parameter when specifying object_audit_trail as the {audit_trail_type}.
                Provide a comma-separated list of one or more object names to retrieve their audit details.
                For example, objects=product__v,country__v. If omitted, defaults to all objects.
            events (str, optional): This is an optional parameter when specifying object_audit_trail or
                document_audit_trail as the {audit_trail_type}. Provide a comma-separated list of one or more audit events
                to retrieve their audit details. For example, events=Edit,Delete,TaskAssignment.
                If omitted, defaults to all audit events.

        Returns:
            dict: The JSON response containing audit details or job information if format_result is 'csv'
        """
        url = f"api/{self.client.LatestAPIversion}/audittrail/{audit_trail_type}"

        params = {}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        if all_dates:
            params["all_dates"] = "true"
        if format_result:
            params["format_result"] = format_result
        if limit != 200:
            params["limit"] = str(limit)
        if offset != 0:
            params["offset"] = str(offset)
        if objects:
            params["objects"] = objects
        if events:
            params["events"] = events

        return self.client.api_call(url, params=params)

    def retrieve_document_audit_history(
        self,
        doc_id: str,
        start_date: str = None,
        end_date: str = None,
        format_result: str = None,
        limit: int = 200,
        offset: int = 0,
        events: str = None,
    ):
        """
        Retrieves complete audit history for a single document.

        Corresponds to GET /api/{version}/objects/documents/{doc_id}/audittrail

        Args:
            doc_id (str): The document ID for which to retrieve audit history.
            start_date (str, optional): Specify a start date to retrieve audit history.
                Dates must be YYYY-MM-DDTHH:MM:SSZ format. If omitted, defaults to the Vault's creation date.
            end_date (str, optional): Specify an end date to retrieve audit history.
                Dates must be YYYY-MM-DDTHH:MM:SSZ format. If omitted, defaults to today's date.
            format_result (str, optional): To request a CSV file of your audit history, use 'csv'.
                The CSV file ignores the start_date and end_date.
            limit (int, optional): Paginate the results by specifying the maximum number of histories per page.
                This can be any value between 1 and 1000. If omitted, defaults to 200.
            offset (int, optional): Paginate the results displayed per page by specifying the amount of offset.
                For example, if you are viewing the first 50 results (page 1) and want to see the next page,
                set this to offset=51. If omitted, defaults to 0.
            events (str, optional): Provide a comma-separated list of one or more audit events to retrieve
                their audit history. The values passed to this parameter are case sensitive.
                For example, events=WorkflowCompletion,TaskAssignment. If omitted, defaults to all audit events.

        Returns:
            dict: The JSON response containing the document's audit history
        """
        url = (
            f"api/{self.client.LatestAPIversion}/objects/documents/{doc_id}/audittrail"
        )

        params = {}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        if format_result:
            params["format_result"] = format_result
        if limit != 200:
            params["limit"] = str(limit)
        if offset != 0:
            params["offset"] = str(offset)
        if events:
            params["events"] = events

        return self.client.api_call(url, params=params)

    def retrieve_object_audit_history(
        self,
        object_name: str,
        object_record_id: str,
        start_date: str = None,
        end_date: str = None,
        format_result: str = None,
        limit: int = 200,
        offset: int = 0,
        events: str = None,
    ):
        """
        Retrieves complete audit history for a single object record.

        Corresponds to GET /api/{version}/vobjects/{object_name}/{object_record_id}/audittrail

        Vault does not audit individual field values for newly created records. For example,
        the audit trail for a new Product record would only include a single entry, and the
        Event Description would be "Product: CholeCap created". When a user deletes an object
        record, the audit trail captures all field values.

        Args:
            object_name (str): The name__v of the object for which to retrieve audit history.
            object_record_id (str): The object record ID for which to retrieve audit history.
            start_date (str, optional): Specify a start date to retrieve audit history.
                Dates must be YYYY-MM-DDTHH:MM:SSZ format. If omitted, defaults to the Vault's creation date.
            end_date (str, optional): Specify an end date to retrieve audit history.
                Dates must be YYYY-MM-DDTHH:MM:SSZ format. If omitted, defaults to today's date.
            format_result (str, optional): To request a CSV file of your audit history, use 'csv'.
            limit (int, optional): Paginate the results by specifying the maximum number of histories per page.
                This can be any value between 1 and 1000. If omitted, defaults to 200.
            offset (int, optional): Paginate the results displayed per page by specifying the amount of offset.
                For example, if you are viewing the first 50 results (page 1) and want to see the next page,
                set this to offset=51. If omitted, defaults to 0.
            events (str, optional): Provide a comma-separated list of one or more audit events to retrieve
                their audit history. The values passed to this parameter are case sensitive.
                For example, events=Copy,Edit,Delete. If omitted, defaults to all audit events.

        Returns:
            dict: The JSON response containing the object record's audit history
        """
        url = f"api/{self.client.LatestAPIversion}/vobjects/{object_name}/{object_record_id}/audittrail"

        params = {}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        if format_result:
            params["format_result"] = format_result
        if limit != 200:
            params["limit"] = str(limit)
        if offset != 0:
            params["offset"] = str(offset)
        if events:
            params["events"] = events

        return self.client.api_call(url, params=params)

    def retrieve_all_debug_logs(
        self, user_id: str = None, include_inactive: bool = False
    ):
        """
        Retrieves all debug log sessions in the authenticated Vault.

        Corresponds to GET /api/{version}/logs/code/debug

        Args:
            user_id (str, optional): Filter results to retrieve the debug log for this user ID only.
                If omitted, this request retrieves debug logs for all users in the Vault.
            include_inactive (bool, optional): Set to true to include debug log sessions with a
                status of inactive__sys in the response. If omitted, defaults to false and
                inactive sessions are not included in the response.

        Returns:
            dict: The JSON response containing information about all debug logs
        """
        url = f"api/{self.client.LatestAPIversion}/logs/code/debug"

        params = {}
        if user_id:
            params["user_id"] = user_id
        if include_inactive:
            params["include_inactive"] = "true"

        return self.client.api_call(url, params=params)

    def retrieve_single_debug_log(self, debug_log_id: str):
        """
        Retrieves details about a specific debug log.

        Corresponds to GET /api/{version}/logs/code/debug/{id}

        Args:
            debug_log_id (str): The ID of the debug log to retrieve.

        Returns:
            dict: The JSON response containing information about the specified debug log
        """
        url = f"api/{self.client.LatestAPIversion}/logs/code/debug/{debug_log_id}"
        return self.client.api_call(url)

    def download_debug_log_files(self, debug_log_id: str):
        """
        Downloads all of a debug log's files.

        Corresponds to GET /api/{version}/logs/code/debug/{id}/files

        On SUCCESS, Vault begins a download of the files for the specified debug log.
        The files are packaged in a ZIP file with the file name:
        vaultjavasdk_{user_id}_debuglogs_{MM-DD-YYYY}.zip.

        Args:
            debug_log_id (str): The ID of the debug log to download.

        Returns:
            bytes: The binary content of the ZIP file containing debug log files
        """
        url = f"api/{self.client.LatestAPIversion}/logs/code/debug/{debug_log_id}/files"
        return self.client.api_call(url, binary_response=True)

    def create_debug_log(
        self,
        name: str,
        user_id: str,
        log_level: str = "all__sys",
        class_filters: List[str] = None,
    ):
        """
        Creates a new debug log session for a user.

        Corresponds to POST /api/{version}/logs/code/debug

        Debug logs have the following limits:
        - Maximum one (1) debug log per user
        - Maximum 20 debug logs per Vault

        Args:
            name (str): The UI-friendly name for this debug log, visible to Admins in the Vault UI.
                Maximum 128 characters.
            user_id (str): The ID of the user who will trigger entries into this debug log.
            log_level (str, optional): The level of error messages to capture in this log.
                Choose one of the following: all__sys (default), exception__sys, error__sys,
                warn__sys, info__sys, debug__sys.
            class_filters (List[str], optional): Class filters allow you to restrict debug log entries
                to only include entries for specific classes. To include class filters for this debug log,
                include an array or comma-separated list of fully-qualified class names.
                For example, com.veeva.vault.custom.triggers.HelloWorld.

        Returns:
            dict: The JSON response containing the ID of the created debug log
        """
        url = f"api/{self.client.LatestAPIversion}/logs/code/debug"

        data = {"name": name, "user_id": user_id, "log_level": log_level}

        if class_filters:
            if isinstance(class_filters, list):
                data["class_filters"] = ",".join(class_filters)
            else:
                data["class_filters"] = class_filters

        return self.client.api_call(url, method="POST", data=data)

    def reset_debug_log(self, debug_log_id: str):
        """
        Deletes all existing log files and resets the expiration date to 30 days from today.

        Corresponds to POST /api/{version}/logs/code/debug/{id}/actions/reset

        Args:
            debug_log_id (str): The ID of the debug log to reset.

        Returns:
            dict: The JSON response indicating success or failure
        """
        url = f"api/{self.client.LatestAPIversion}/logs/code/debug/{debug_log_id}/actions/reset"
        return self.client.api_call(url, method="POST")

    def delete_debug_log(self, debug_log_id: str):
        """
        Deletes a debug log and all log files.

        Corresponds to DELETE /api/{version}/logs/code/debug/{id}

        Args:
            debug_log_id (str): The ID of the debug log to delete.

        Returns:
            dict: The JSON response indicating success or failure
        """
        url = f"api/{self.client.LatestAPIversion}/logs/code/debug/{debug_log_id}"
        return self.client.api_call(url, method="DELETE")

    def retrieve_all_profiling_sessions(self):
        """
        Lists all SDK request profiling sessions in the currently authenticated Vault.

        Corresponds to GET /api/{version}/code/profiler

        The authenticated user must have the Admin: Logs: Vault Java SDK permission
        to perform operations on profiling sessions.

        Returns:
            dict: The JSON response containing information about all profiling sessions
        """
        url = f"api/{self.client.LatestAPIversion}/code/profiler"
        return self.client.api_call(url)

    def retrieve_profiling_session(self, session_name: str):
        """
        Retrieves details about a specific SDK request profiling session.

        Corresponds to GET /api/{version}/code/profiler/{session_name}

        Args:
            session_name (str): The name of the session, for example, baseline__c.

        Returns:
            dict: The JSON response containing information about the specified profiling session
        """
        url = f"api/{self.client.LatestAPIversion}/code/profiler/{session_name}"
        return self.client.api_call(url)

    def create_profiling_session(
        self, label: str, user_id: str = None, description: str = None
    ):
        """
        Creates a new SDK request profiling session.

        Corresponds to POST /api/{version}/code/profiler

        Vault starts the profiling session immediately on creation. Profiling sessions run
        for either 20 minutes or up to 10,000 SDK requests, whichever comes first. Only one
        profiling session can be active at a time. Each Vault can only retain profiling session
        data for up to 10 sessions.

        Args:
            label (str): The UI label for this request.
            user_id (str, optional): The user ID of the user to associate with this session.
                When specified, this SDK profiling session runs only for this user.
                If omitted, defaults to null which runs the session for all users.
            description (str, optional): An Admin-facing description of the session.

        Returns:
            dict: The JSON response containing the ID and name of the created session
        """
        url = f"api/{self.client.LatestAPIversion}/code/profiler"

        data = {"label": label}
        if user_id:
            data["user_id"] = user_id
        if description:
            data["description"] = description

        return self.client.api_call(url, method="POST", data=data)

    def end_profiling_session(self, session_name: str):
        """
        Terminates a profiling session early.

        Corresponds to POST /api/{version}/code/profiler/{session_name}/actions/end

        By default, profiling sessions run for either 20 minutes or up to 10,000 SDK requests,
        whichever comes first. Once ended, a session's status is processing__sys while Vault
        prepares the data, which may take about 15 minutes.

        Args:
            session_name (str): The name of the session, for example, baseline__c.

        Returns:
            dict: The JSON response indicating success or failure
        """
        url = f"api/{self.client.LatestAPIversion}/code/profiler/{session_name}/actions/end"
        return self.client.api_call(url, method="POST")

    def delete_profiling_session(self, session_name: str):
        """
        Deletes an inactive profiling session and all associated data.

        Corresponds to DELETE /api/{version}/code/profiler/{session_name}

        This deletes the session and all data associated with the session.
        Inactive sessions have a status of complete__sys.

        Args:
            session_name (str): The name of the session, for example, baseline__c.

        Returns:
            dict: The JSON response indicating success or failure
        """
        url = f"api/{self.client.LatestAPIversion}/code/profiler/{session_name}"
        return self.client.api_call(url, method="DELETE")

    def download_profiling_session_results(self, session_name: str):
        """
        Downloads the Profiler Log for a specific profiling session.

        Corresponds to GET /api/{version}/code/profiler/{session_name}/results

        A profiling session log is a CSV which contains one row for each SDK request,
        with a maximum of 100,000 rows.

        Args:
            session_name (str): The name of the session, for example, baseline__c.

        Returns:
            bytes: The binary content of the ZIP file containing the profiling results
        """
        url = f"api/{self.client.LatestAPIversion}/code/profiler/{session_name}/results"
        return self.client.api_call(url, binary_response=True)

    def retrieve_email_notification_histories(
        self,
        start_date: str = None,
        end_date: str = None,
        all_dates: bool = False,
        format_result: str = None,
        limit: int = 200,
        offset: int = 0,
    ):
        """
        Retrieves details about the email notifications sent by Vault.

        Corresponds to GET /api/{version}/notifications/histories

        Details include the notification date, recipient, subject, and delivery status.
        In the UI, this information is available in Admin > Operations > Email Notification Status.

        Args:
            start_date (str, optional): Specify a start date to retrieve notification history.
                This date cannot be more than 3 months ago. To retrieve older email notifications,
                use the all_dates parameter instead. Dates must be in YYYY-MM-DD or YYYY-MM-DDTHH:mm:ssZ format.
                If time is omitted (THH:mm:ssZ), defaults to the start of the day.
                If start_date is omitted entirely, defaults to the start of the previous day.
                If you've specified a start_date, you must also specify an end_date.
            end_date (str, optional): Specify an end date to retrieve notification history.
                This date cannot be more than 30 days away from the specified start_date.
                Dates must be in YYYY-MM-DD or YYYY-MM-DDTHH:mm:ssZ format.
                If time is omitted (THH:mm:ssZ), defaults to the time of the API request.
                If you've specified an end_date, you must also specify a start_date.
            all_dates (bool, optional): Set to true to request notification history for all dates.
                This request starts a job to prepare a downloadable .zip of CSV files of the entire
                notification history by year. When requesting a full notification history, you must
                leave start_date and end_date blank and set format_result to csv. You can request an
                export of notification history for all_dates once every 24 hours.
            format_result (str, optional): To request a downloadable CSV file of your notification history,
                set this parameter to 'csv'. The response contains a jobId to retrieve the job status,
                which provides a link to download the CSV file. If omitted, the API returns a JSON response
                with notification history and does not start a job. If all_dates is true, this parameter must be 'csv'.
            limit (int, optional): Paginate the results by specifying the maximum number of histories per page.
                This can be any value between 1 and 1000. If omitted, defaults to 200.
            offset (int, optional): Paginate the results displayed per page by specifying the amount of offset.
                If omitted, defaults to 0.

        Returns:
            dict: The JSON response containing email notification histories or job information if format_result is 'csv'
        """
        url = f"api/{self.client.LatestAPIversion}/notifications/histories"

        params = {}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        if all_dates:
            params["all_dates"] = "true"
        if format_result:
            params["format_result"] = format_result
        if limit != 200:
            params["limit"] = str(limit)
        if offset != 0:
            params["offset"] = str(offset)

        return self.client.api_call(url, params=params)

    def download_daily_api_usage(self, date: str, log_format: str = "csv"):
        """
        Retrieves the API Usage Log for a single day, up to 30 days in the past.

        Corresponds to GET /api/{version}/logs/api_usage?date=YYYY-MM-DD

        The log contains information such as user name, user ID, remaining burst limit,
        and the endpoint called. Users with the Admin: Logs: API Usage Logs permission
        can access these logs.

        Note that the daily logs may have a delay of about 15 minutes. The logs are designed
        for troubleshooting burst limits and discovering which of your integrations are
        causing you to hit the limit. These logs should not be used for auditing.

        Args:
            date (str): The day to retrieve the API Usage log. Date is in UTC and follows
                the format YYYY-MM-DD. Date cannot be more than 30 days in the past.
            log_format (str, optional): Specify the format to download. Possible values are
                'csv' or 'logfile'. If omitted, defaults to 'csv'. Note that this call always
                downloads a ZIP file. This parameter only changes the format of the file
                contained within the ZIP.

        Returns:
            bytes: The binary content of the ZIP file containing the API usage log
        """
        url = f"api/{self.client.LatestAPIversion}/logs/api_usage"

        params = {"date": date}
        if log_format != "csv":
            params["log_format"] = log_format

        return self.client.api_call(url, params=params, binary_response=True)

    def download_sdk_runtime_log(self, date: str, log_format: str = "csv"):
        """
        Retrieves the Runtime Log for a single day, up to 30 days in the past.

        Corresponds to GET /api/{version}/logs/code/runtime?date=YYYY-MM-DD

        Users with the Admin: Logs: Vault Java SDK Logs permission can access these logs.
        The runtime logs create entries 15 minutes after the Vault Java SDK transaction completes.

        Args:
            date (str): The day to retrieve the runtime log. Date is in UTC and follows
                the format YYYY-MM-DD. Date cannot be more than 30 days in the past.
            log_format (str, optional): Specify the format to download. Possible values are
                'csv' or 'logfile'. If omitted, defaults to 'csv'. This request always downloads
                a ZIP file; this parameter only changes the format of the file contained within the ZIP.

        Returns:
            bytes: The binary content of the ZIP file containing the SDK runtime log
        """
        url = f"api/{self.client.LatestAPIversion}/logs/code/runtime"

        params = {"date": date}
        if log_format != "csv":
            params["log_format"] = log_format

        return self.client.api_call(url, params=params, binary_response=True)
