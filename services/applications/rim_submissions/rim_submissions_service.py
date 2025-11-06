from typing import Dict, Any, Optional, Union, BinaryIO
import json


class RIMSubmissionsService:
    """
    Service class for interacting with the Veeva Vault RIM Submissions application.

    This service provides methods for managing content plans and submissions.
    """

    def __init__(self, client):
        """
        Initialize the RIMSubmissionsService with a VaultClient instance.

        Args:
            client: An initialized VaultClient instance for API communication
        """
        self.client = client

    def copy_into_content_plan(
        self, source_id: str, target_id: str, order: int, copy_documents: bool
    ) -> Dict[str, Any]:
        """
        This API allows you to copy a content plan section or item to reuse existing content and prevent
        duplicate work. For example, you may want to copy a clinical study or quality section and its
        matched documents for a similar submission to a different application.

        This API functionality has the same behavior and limitations as copying through the Content Plan
        Hierarchy Viewer in the Vault UI. Learn more about copying into content plans in Vault Help.

        Args:
            source_id: The ID of the content plan or content plan item to copy.
            target_id: The ID of the parent content plan, which is where the source content plan will be copied under.
                     Cannot be inactive.
            order: An integer indicating the position in the target content plan where the source content
                  plan will be copied. A value of 1 indicates the first position in the target content plan.
            copy_documents: If true, matched documents are included in the copy. If false, matched documents
                          are not included in the copy. Cannot be omitted.

        Returns:
            A dictionary containing the response data. For content plans, it includes a job_id for the
            asynchronous process. For content plan items, it includes the createdCPIRecordId of the new item.
        """
        endpoint = (
            f"api/{self.client.LatestAPIversion}/app/rim/content_plans/actions/copyinto"
        )

        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        data = {
            "source_id": source_id,
            "target_id": target_id,
            "order": order,
            "copy_documents": copy_documents,
        }

        return self.client.api_call(
            endpoint=endpoint, method="POST", headers=headers, json=data
        )
