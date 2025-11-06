import json
from .base_service import BaseObjectService


class ObjectRollupService(BaseObjectService):
    """
    Service class for handling Veeva Vault object roll-up field operations.

    Roll-up fields calculate values based on related child records, supporting
    functions like minimum, maximum, count, or sum of source field values.
    """

    def recalculate_rollup_fields(self, object_name, record_id=None, fields=None):
        """
        Recalculates roll-up field values for a specific object record or all roll-up fields
        for the specified object.

        POST /api/{version}/vobjects/{object_name}/actions/recalculaterollups
        OR
        POST /api/{version}/vobjects/{object_name}/{record_id}/actions/rolluprecalculate

        Args:
            object_name (str): API name of the object
            record_id (str, optional): ID of the record to recalculate. If not provided,
                                     all roll-up fields on the object are recalculated.
            fields (list, optional): List of specific roll-up fields to recalculate

        Returns:
            dict: API response with job ID or success message

        Notes:
            - You can configure up to 25 Roll-up fields on a parent object
            - When performing a full recalculation, Vault evaluates all Roll-up fields asynchronously
            - Record triggers on parent records do not fire when Roll-up fields are updated
            - This endpoint is equivalent to the Recalculate Roll-up Fields action in the Vault UI
            - While a recalculation is running, Admins cannot start another recalculation
        """
        if record_id:
            url = f"api/{self.client.LatestAPIversion}/vobjects/{object_name}/{record_id}/actions/rolluprecalculate"
        else:
            url = f"api/{self.client.LatestAPIversion}/vobjects/{object_name}/actions/recalculaterollups"

        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        data = {}
        if fields:
            data["fields"] = fields if isinstance(fields, list) else [fields]

        return self.client.api_call(
            url, method="POST", headers=headers, data=json.dumps(data) if data else None
        )

    def retrieve_rollup_field_recalculation_status(self, object_name, job_id=None):
        """
        Retrieves the status of a roll-up field recalculation job.

        GET /api/{version}/vobjects/{object_name}/actions/recalculaterollups
        OR
        GET /api/{version}/vobjects/{object_name}/actions/rolluprecalculate/{job_id}

        Args:
            object_name (str): API name of the object
            job_id (str, optional): ID of the recalculation job. If not provided,
                                   the status of any active recalculation for the object is returned.

        Returns:
            dict: Status of the recalculation job (RUNNING or NOT_RUNNING)
        """
        if job_id:
            url = f"api/{self.client.LatestAPIversion}/vobjects/{object_name}/actions/rolluprecalculate/{job_id}"
        else:
            url = f"api/{self.client.LatestAPIversion}/vobjects/{object_name}/actions/recalculaterollups"

        return self.client.api_call(url)
