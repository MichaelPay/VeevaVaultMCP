import pandas as pd


class JobsService:
    """
    Service class for managing jobs in Veeva Vault.

    This service provides methods to interact with job-related API endpoints,
    allowing retrieval of job status, history, and monitors, as well as starting jobs.
    """

    def __init__(self, client):
        """
        Initialize with a VaultClient instance

        Args:
            client: An initialized VaultClient instance for API communication
        """
        self.client = client

    def retrieve_job_status(self, job_id):
        """
        Retrieve the status of a job.

        After submitting a request, you can query your Vault to determine the status of the request.
        To do this, you must have a valid job_id for a job previously requested through the API.

        Corresponds to GET /api/{version}/services/jobs/{job_id}

        Note:
            The Job Status endpoint can only be requested once every 10 seconds for each job_id.
            When this limit is reached, Vault returns API_LIMIT_EXCEEDED.

        Example Jobs:
            - Binder Export
            - Import Submission
            - Export Submission
            - Create EDL
            - Deploy Package
            - Deep Copy Object Record
            - Cascade Delete Object Record
            - Export Documents

        Args:
            job_id (int): The ID of the job, returned from the original job request.

        Returns:
            dict: The JSON response containing job status information, including:
                - id: The job_id field value for the job.
                - status: The status of the job. Possible statuses include SCHEDULED, QUEUED, RUNNING,
                  SUCCESS, ERRORS_ENCOUNTERED, QUEUEING, CANCELLED, and MISSED_SCHEDULE.
                - method: The HTTP method used in the request.
                - links: Once the job is finished, use these endpoints and methods to retrieve other job details.
                - progress: If the retrieved job is a custom job created with the Vault Java SDK, this array
                  contains a summary of the number of job tasks (size) and their status.
                - created_by: The id field value of the user who started the job.
                - created_date: The date and time when the job was requested.
                - run_start_date: The date and time when the export job started.
                - run_end_date: The date and time when the export job finished.

        Note:
            All DateTime values for scheduled jobs are in the Vault time zone for the currently
            authenticated user.
        """
        url = f"api/{self.client.LatestAPIversion}/services/jobs/{job_id}"
        return self.client.api_call(url)

    def retrieve_sdk_job_tasks(self, job_id, limit=50, offset=0):
        """
        Retrieve the tasks associated with an SDK job.

        Corresponds to GET /api/{version}/services/jobs/{job_id}/tasks

        Args:
            job_id (int): The ID of the SDK job, returned from the original job request.
            limit (int, optional): The maximum number of tasks to return. Defaults to 50.
            offset (int, optional): The offset for pagination. Defaults to 0.

        Returns:
            dict: The JSON response containing:
                - responseStatus: "SUCCESS" if successful
                - url: The URL of the request with pagination parameters
                - responseDetails: Object containing pagination details (total, limit, offset)
                - job_id: The ID of the job
                - tasks: Array of task objects, each with:
                    - id: The task ID
                    - state: The state of the task (e.g., "SUCCESS", "RUNNING")
        """
        url = f"api/{self.client.LatestAPIversion}/services/jobs/{job_id}/tasks"

        params = {"limit": limit, "offset": offset}

        return self.client.api_call(url, params=params)

    def retrieve_job_histories(
        self, start_date=None, end_date=None, status=None, limit=50, offset=0
    ):
        """
        Retrieve a history of all completed jobs in the authenticated Vault.

        A completed job is any job which has started and finished running, including jobs which
        did not complete successfully. In-progress or queued jobs do not appear here.

        Corresponds to GET /api/{version}/services/jobs/histories

        Args:
            start_date (str, optional): Sets the date to start retrieving completed jobs, in the format
                YYYY-MM-DDTHH:MM:SSZ. For example, for 7AM on January 15, 2016, use 2016-01-15T07:00:00Z.
                If omitted, defaults to the first completed job.
            end_date (str, optional): Sets the date to end retrieving completed jobs, in the format
                YYYY-MM-DDTHH:MM:SSZ. If omitted, defaults to the current date and time.
            status (str, optional): Filter to only retrieve jobs in a certain status. Allowed values are
                success, errors_encountered, failed_to_run, missed_schedule, cancelled.
                If omitted, retrieves all statuses.
            limit (int, optional): Paginate the results by specifying the maximum number of histories
                per page in the response. This can be any value between 1 and 200. Defaults to 50.
            offset (int, optional): Paginate the results displayed per page by specifying the amount of
                offset from the first job history returned. Defaults to 0.

        Returns:
            dict: The JSON response containing:
                - responseStatus: "SUCCESS" if successful
                - responseMessage: "OK" if successful
                - url: The URL of the request with pagination parameters
                - responseDetails: Object containing pagination details (total, limit, offset, next_page)
                - jobs: Array of job history objects, each with:
                    - job_id: The ID of the job
                    - title: The title of the job
                    - status: The status of the job
                    - created_by: The ID of the user who created the job
                    - created_date: The date and time when the job was created
                    - modified_by: The ID of the user who last modified the job
                    - modified_date: The date and time when the job was last modified
                    - run_start_date: The date and time when the job started running
                    - run_end_date: The date and time when the job finished running
        """
        url = f"api/{self.client.LatestAPIversion}/services/jobs/histories"

        params = {"limit": limit, "offset": offset}

        if start_date:
            params["start_date"] = start_date

        if end_date:
            params["end_date"] = end_date

        if status:
            params["status"] = status

        return self.client.api_call(url, params=params)

    def retrieve_job_monitors(
        self, start_date=None, end_date=None, status=None, limit=50, offset=0
    ):
        """
        Retrieve monitors for jobs which have not yet completed in the authenticated Vault.

        An uncompleted job is any job which has not finished running, such as scheduled, queued,
        or actively running jobs. Completed jobs do not appear here.

        Corresponds to GET /api/{version}/services/jobs/monitors

        Args:
            start_date (str, optional): Sets the date to start retrieving uncompleted jobs, based on the
                date and time the job instance was created. Value must be in the format YYYY-MM-DDTHH:MM:SSZ.
                If omitted, defaults to the first completed job.
            end_date (str, optional): Sets the date to end retrieving uncompleted jobs, based on the
                date and time the job instance was created. Value must be in the format YYYY-MM-DDTHH:MM:SSZ.
                If omitted, defaults to the current date and time.
            status (str, optional): Filter to only retrieve jobs in a certain status. Allowed values are
                scheduled, queued, running. If omitted, retrieves all statuses.
            limit (int, optional): Paginate the results by specifying the maximum number of jobs
                per page in the response. This can be any value between 1 and 200. Defaults to 50.
            offset (int, optional): Paginate the results displayed per page by specifying the amount of
                offset from the first job instance returned. Defaults to 0.

        Returns:
            dict: The JSON response containing:
                - responseStatus: "SUCCESS" if successful
                - responseMessage: "OK" if successful
                - url: The URL of the request with pagination parameters
                - responseDetails: Object containing pagination details (total, limit, offset)
                - jobs: Array of job monitor objects, each with:
                    - job_id: The ID of the job
                    - title: The title of the job
                    - status: The status of the job
                    - created_by: The ID of the user who created the job
                    - created_date: The date and time when the job was created
                    - modified_by: The ID of the user who last modified the job
                    - modified_date: The date and time when the job was last modified
                    - run_start_date: The date and time when the job is scheduled to start
        """
        url = f"api/{self.client.LatestAPIversion}/services/jobs/monitors"

        params = {"limit": limit, "offset": offset}

        if start_date:
            params["start_date"] = start_date

        if end_date:
            params["end_date"] = end_date

        if status:
            params["status"] = status

        return self.client.api_call(url, params=params)

    def start_job(self, job_id):
        """
        Moves up a scheduled job instance to start immediately.

        Each time a user calls this API, Vault cancels the scheduled instance of the specified job
        for the current interval. For example, if a job is scheduled to run daily at 11PM PST, calling
        this API against it at 4PM PST will cause the job to not run as scheduled at 11PM PST the same day.
        Vault will resume running the job at 11PM PST the next day regardless of how many times this API
        is called before 11PM PST the previous day.

        This is analogous to the Start Now option in the Vault UI.

        Corresponds to POST /api/{version}/services/jobs/start_now/{job_id}

        Args:
            job_id (int): The ID of the scheduled job instance to start.

        Returns:
            dict: The JSON response containing:
                - responseStatus: "SUCCESS" if successful
                - url: The URL to check job status
                - job_id: The ID of the job that was started
        """
        url = f"api/{self.client.LatestAPIversion}/services/jobs/start_now/{job_id}"

        return self.client.api_call(url, method="POST")
