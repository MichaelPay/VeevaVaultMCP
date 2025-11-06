<!-- 
VaultAPIDocs Section: # RIM Submissions
Original Line Number: 42839
Generated: August 30, 2025
Part 35 of 38
-->

# RIM Submissions

To use this API, you must have Veeva RIM Submissions. Learn more about [RIM Submissions in Vault Help](https://regulatory.veevavault.help/en/lr/30704).

## Copy into Content Plan

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Content-Type: application/json" \
https://myvault.veevavault.com/api/v25.2/app/rim/content_plans/actions/copyinto
'''

> Response: Content Plan

'''
{
   "responseStatus": "WARNING",
   "warnings": [
       {
           "type": "TEMPLATE_MISMATCH",
           "message": "The templates of the source and target do not align."
       },
       {
           "type": "LEVEL_MISMATCH",
           "message": "Level of the source record does not match the level of the target location."
       }
   ],
   "job_id": 104448
}
'''

> Response: Content Plan Item

'''
{
   "responseStatus": "WARNING",
   "warnings": [
       {
           "type": "LEVEL_MISMATCH",
           "message": "Level of the source record does not match the level of the target location."
       },
       {
           "type": "TEMPLATE_MISMATCH",
           "message": "The templates of the source and target do not align."
       }
   ],
   "createdCPIRecordId": "0EI000000004001"
}
'''

This API allows you to copy a content plan section or item to reuse existing content and prevent duplicate work. For example, you may want to copy a clinical study or quality section and its matched documents for a similar submission to a different application.

This API functionality has the same behavior and limitations as copying through the Content Plan Hierarchy Viewer in the Vault UI. Learn more about [copying into content plans in Vault Help](https://regulatory.veevavault.help/en/lr/71665).

POST `/api/{version}/app/rim/content_plans/actions/copyinto`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### Body Parameters

Name

Description

`source_id`

The ID of the content plan or content plan item to copy.

`target_id`

The ID of the parent content plan, which is where the source content plan will be copied under. Cannot be inactive.

`order`

An integer indicating the position in the target content plan where the source content plan will be copied. A value of `1` indicates the first position in the target content plan.

`copy_documents`

If `true`, matched documents are included in the copy. If `false`, matched documents are not included in the copy. Cannot be omitted.

#### Response Details

Copying a content plan is an asynchronous process which provides a `job_id`. When the copy is complete, you’ll receive an email notification.

Copying a content plan item is a synchronous process which provides the `createdCPIRecordId` of the newly copied content plan item.
