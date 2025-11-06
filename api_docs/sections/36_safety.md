<!-- 
VaultAPIDocs Section: # Safety
Original Line Number: 42935
Generated: August 30, 2025
Part 36 of 38
-->

# Safety

To use this API, you must have Veeva Safety. Learn more about Veeva Safety in [Veeva Safety Help](https://safety.veevavault.help/en/lr/).

## Intake

### Intake Inbox Item

> Request

'''
curl --location --request POST 'https://myvault.veevavault.com/api/v25.2/app/safety/intake/inbox-item' \
--header 'Content-Type: multipart/form-data' \
--header 'Authorization: {SESSION_ID}' \
--form 'file=@"/directory/labrinone_literature_case.xml"' \
--form 'origin-organization="vertio_biopharma__c"' \
--form 'format="e2br3__v"' \
--form 'organization="vault_customer__v"'
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "url": "/api/v25.2/app/safety/intake/status?inbound_id=V29000000004001",
    "intake_id": "V29000000004001"
}
'''

Use the following endpoint to import an Inbox Item from an E2B (R2) or E2B (R3) file containing one or more Individual Case Safety Reports (ICSRs):

POST `/api/{version}/app/safety/intake/inbox-item`

#### Headers

Name

Description

`Content-Type`

`multipart/form-data`

#### Body Parameters

Name

Description

`file`

The filepath of the E2B file to be imported.

`origin-organization`

(Optional) The Vault API Name for the Organization sending the E2B file. This parameter sets the Origin Organization on the Inbound Transmission. If no value is provided, the Origin Organization is left blank.

`format`

The format of the file being imported. This must match the Vault API Name of the Inbound Transmission Format picklist value. Must be an E2B format.

`organization`

(Optional) To specify which organization to send the Case to, enter the Vault API Name for the Organization record. If no value is provided, the Organization is set to `vault_customer__v`. Note that the Organization record type must be Sponsor.

`transmission-profile`

(Optional) The Vault API Name of the Transmission Profile to be used for E2B Intake. These parameters are used for Narrative Template Override and Inbox Item Auto-Promotion. The Transmission Profile record type must be Connection. This parameter is required for Automated Case Promotion (see [Veeva Safety Help](https://safety.veevavault.help/en/lr/01131/) for more information). If no `transmission-profile` is specified, Vault will use the parameters on the `general_api_profile__v`.

#### Response Details

On `SUCCESS`, the response includes the following information:

Name

Description

`url`

The URL to retrieve the current status of the import request.

`intake_id`

The Inbound Transmission ID of the E2B import.

On `FAILURE`, the response returns a message describing the reason for the failure.

### Intake Imported Case

> Request

'''
curl --location --request POST 'https://myvault.veevavault.com/api/v25.2/app/safety/intake/imported-case' \
--header 'Authorization: {SESSION_ID}' \
--header 'Content-Type: multipart/form-data' \
--form 'file=@"/directory/cholecap_vaers_literature_case.xml"' \
--form 'format="e2br3__v"' \
--form 'organization="verteo_biopharma__c"' \
--form 'origin-organization="fda__v"'
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "url": "/api/v25.2/app/safety/intake/status?inbound_id=V29000000005001",
    "intake_id": "V29000000005001"
}
'''

Use the following endpoint to import an Imported Case from an E2B (R2) or E2B (R3) file containing one or more Individual Case Safety Reports (ICSRs):

POST `/api/{version}/app/safety/intake/imported-case`

#### Headers

Name

Description

`Content-Type`

`multipart/form-data`

#### Body Parameters

Name

Description

`file`

The filepath of the E2B file to be imported.

`origin-organization`

(Optional) The Vault API Name for the Organization sending the E2B file. This parameter sets the Origin Organization on the Inbound Transmission. If no value is provided, the Origin Organization is left blank.

`format`

The format of the file being imported. This must match the Vault API Name of the Inbound Transmission Format picklist value. Must be an E2B format or `other__v`. If `other__v`, the system does not attempt E2B import or forms processing and instead creates an empty Inbox Item linked to the source document.

`organization`

(Optional) To specify which organization to send the Case to, enter the Vault API Name for the Organization record. If no value is provided, the Organization is set to `vault_customer__v`. Note that the Organization record type must be Sponsor.

#### Response Details

On `SUCCESS`, the response includes the following information:

Name

Description

`url`

The URL to retrieve the current status of the import request.

`intake_id`

The Inbound Transmission ID of the E2B import.

On `FAILURE`, the response returns a message describing the reason for the failure.

### Retrieve Intake Status

> Request

'''
curl --location --request GET 'https://myvault.veevavault.com/api/v25.2/app/safety/intake/status?inbound_id=V29000000005001' \
--header 'Authorization: {SESSION_ID}' \
--header 'Content-Type: multipart/form-data' \
--form 'file=@"/directory/e2b_r3_restolar.xml"' \
--form 'format="e2br3__v"'
'''

> Response

'''
{
    "status": "complete",
    "ack-retrieval": "/api/v25.2/app/safety/intake/ack?inbound_id=V29000000005001",
    "inbound-transmission": "V29000000005001",
    "inbound-document": "7_0_1",
    "number-of-icsrs": 1,
    "number-success/warning": 1,
    "number-failures": 0,
    "icsr-details": [
        {
            "icsr": "V2B000000005001",
            "inbound-transmission": "V29000000005001",
            "inbound-document": "7_0_1",
            "ack-retrieval": "/api/v25.2/app/safety/intake/ack?inbound_id=V29000000005001",
            "status": "Success"
        }
    ]
}
'''

Use the following endpoint to retrieve the status of an intake API call:

GET `/api/{version}/app/safety/intake/status`

The Retrieve Intake Status endpoint can be used with the following Safety intake endpoints:

-   Intake Inbox Item
-   Intake Imported Case

#### Headers

Name

Description

`Accept`

`application/json`

#### URL Parameters

Name

Description

`inbound_id`

The Inbound Transmission ID for the ICSR intake job.

#### Response Details

On `SUCCESS`, the response includes the following information:

Name

Description

`status`

Processing status for the intake job.

`ack-retrieval`

URL to retrieve the ACK. This parameter only applies to E2B intake file types.

`inbound-transmission`

ID or link to the Inbound Transmission for the entire intake job.

`inbound-document`

ID or link to the Vault document created from E2B file for the entire intake job.

`number-cases`

Total number of cases found in the intake file, including both successes and failures.

`number-successes`

Number of cases that were imported successfully, including those with warnings.

`number-failures`

Number of cases that failed to import.

`icsr-details`

An array containing details for each individual case within the file. This will be populated with a single entry for single E2B files.

`icsr-details.case`

ID of the Imported Case record. Present only for Imported Case intake jobs.

`icsr-details.inbox-item`

ID of the Inbox Item record. Present only for Inbox Item intake jobs.

`icsr-details.inbound-transmission`

ID of the Inbound Transmission for this case.

`icsr-details.inbound-document`

ID of the Vault document for the case. For multi-case E2B files, the E2B for individual cases is split out into separate documents.

`icsr-details.ack-retrieval`

URL for the ACK for the case. This parameter only applies to E2B intake file types.

`icsr-details.status`

Status of the Imported Case or Inbox Item.

On `FAILURE`, the response returns a message describing the reason for the failure.

### Retrieve ACK

> Request

'''
curl --location --request GET 'https://myvault.veevavault.com/api/v25.2/app/safety/intake/ack?inbound_id=V29000000005001' \
--header 'Authorization: {SESSION_ID}' \
--header 'Content-Type: multipart/form-data' \
--form 'file=@"/directory/e2b_r3_restolar.xml"' \
--form 'format="e2br3__v"'
'''

> Response

'''
<?xml version="1.0" encoding="utf-8"?>
<MCCI_IN200101UV01 xmlns="urn:hl7-org:v3" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="urn:hl7-org:v3 http://eudravigilance.ema.europa.eu/xsd/multicacheschemas/MCCI_IN200101UV01.xsd" ITSVersion="XML_1.0">
    <!--ACK.M.1 - Acknowledgement Batch Number-->
    <id root="2.16.840.1.113883.3.989.2.1.3.20" extension="b4e413b2-7263-48b5-b957-839fea7c7edc"/>
    <!--ACK.M.4 - Date of Message-->
    <creationTime value="20210618154357-0400"/>
    <!--Mandatory element-->
    <responseModeCode code="D"/>
    <interactionId extension="MCCI_IN200101UV01" root="2.16.840.1.113883.1.6"/>
    <MCCI_IN000002UV01>
        <!--ACK.B.r.2 - Local Report Number-->
        <id root="2.16.840.1.113883.3.989.2.1.3.19" extension="VERN-123-123-123"/>
        <!--ACK.M.4 - ACK Date of Batch Transmission-->
        <creationTime value="20210618154357-0400"/>
        <interactionId root="2.16.840.1.113883.1.18" extension="MCCI_IN000002UV01"/>
        <processingCode code="P"/>
        <processingModeCode code="T"/>
        <acceptAckCode code="NE"/>
        <receiver typeCode="RCV">
            <device determinerCode="INSTANCE" classCode="DEV">
                <!--ACK.B.r.3: ICSR Message Receiver Identifier-->
                <id root="2.16.840.1.113883.3.989.2.1.3.16" extension="ICHTEST"/>
            </device>
        </receiver>
        <sender typeCode="SND">
            <device determinerCode="INSTANCE" classCode="DEV">
                <!--ACK.B.r.4: ICSR Message Sender Identifier-->
                <id root="2.16.840.1.113883.3.989.2.1.3.15" extension="DSJP"/>
            </device>
        </sender>
        <attentionLine>
            <!--ACK.B.r.5 - Receipt date-->
            <keyWordText codeSystemVersion="2.0" codeSystem="2.16.840.1.113883.3.989.2.1.1.24" code="1"/>
            <value value="20120720100001+09" xsi:type="TS"/>
        </attentionLine>
        <!--ACK.B.r.6 - Acknowledgement Report Code-->
        <acknowledgement typeCode="CA">
            <targetMessage>
                <!--ACK.B.r.1 - Safety Report ID ICSR Message Number-->
                <id root="2.16.840.1.113883.3.989.2.1.3.1" extension="VERN-123-123-123"/>
            </targetMessage>
            <acknowledgementDetail>
                <!--ACK.B.r.7 - Error/Warning message / comment-->
                <text>[F.r.5 Normal High Value (Unit), mg/dl] inconsistent_unit; [C.5.3, 0105798/01] unable_to_link_study_for_wrong_type; [C.5.1.r.1, 2004-09102-03] unable_to_link_study_for_wrong_type; [C.5.1.r.2, EU] unable_to_link_study_for_wrong_type; [C.5.1.r.1, NL...</text>
            </acknowledgementDetail>
        </acknowledgement>
    </MCCI_IN000002UV01>
    <receiver typeCode="RCV">
        <device determinerCode="INSTANCE" classCode="DEV">
            <!--ACK.M.3 - Acknowledgement Batch Receiver Identifier-->
            <id root="2.16.840.1.113883.3.989.2.1.3.18" extension="DSJP"/>
        </device>
    </receiver>
    <sender typeCode="SND">
        <device determinerCode="INSTANCE" classCode="DEV">
            <!--ACK.M.2 - Acknowledgement Batch Sender Identifier-->
            <id root="2.16.840.1.113883.3.989.2.1.3.17" extension="ICHTEST"/>
        </device>
    </sender>
    <attentionLine>
        <!--ACK.A.2 - Local Message Number-->
        <keyWordText codeSystemVersion="2.0" codeSystem="2.16.840.1.113883.3.989.2.1.1.24" code="2"/>
        <value root="2.16.840.1.113883.3.989.2.1.3.21" extension="TR-000006_b4e413b2-7263-48b5-b957-839fea7c7edc_20210618194357" xsi:type="II"/>
    </attentionLine>
    <attentionLine>
        <!--ACK.A.3 - Date of ICSR Batch Transmission-->
        <keyWordText codeSystemVersion="2.0" codeSystem="2.16.840.1.113883.3.989.2.1.1.24" code="3"/>
        <value value="20120720100000" xsi:type="TS"/>
    </attentionLine>
    <!--ACK.A.4- Transmission Acknowledgment Code-->
    <acknowledgement typeCode="AE">
        <targetBatch>
            <!--ACK.A.1 - ICSR Batch Number -->
            <id root="2.16.840.1.113883.3.989.2.1.3.22" extension="DSJP-B0123456"/>
        </targetBatch>
        <!--ACK.A.5 - Batch Validation Error-->
        <acknowledgementDetail>
            <text>[F.r.5 Normal High Value (Unit), mg/dl] inconsistent_unit; [C.5.3, 0105798/01] unable_to… See B.r.7</text>
        </acknowledgementDetail>
    </acknowledgement>
</MCCI_IN200101UV01>
'''

Use the following endpoint to retrieve the E2B acknowledgement message (ACK) after sending an intake call:

GET `/api/{version}/app/safety/intake/ack`

The Retrieve ACK endpoint can be used with the following Safety intake endpoints:

-   Intake Inbox Item
-   Intake Imported Case

#### Headers

Name

Description

`Accept`

`application/json`

#### URL Parameters

Name

Description

`inbound_id`

The Inbound Transmission ID for the ICSR intake job.

#### Response Details

On `SUCCESS`, the response returns the ACK XML. The ACK is returned in the same E2B format as the intake file.

On `FAILURE`, the response returns a message describing the reason for the failure.

## Intake JSON

> Request

'''
curl --location --request POST 'https://safety.veevavault.com/api/v25.2/app/safety/ai/intake?API_Name=verteo_biopharma' \
--header 'Authorization: {SESSION_ID} '  \
--header ‘Content-Type: application/json’ \
--form 'intake_json=@/C:/Users/Vern/Documents/intake.json'
'''

> Response SUCCESS

'''
{
     “responseStatus” :  “SUCCESS”,
     “jobId” : “69813”,
    “transmissionRecordId”: “V29000000000E09”
}
'''

> Response FAILURE

'''
{
    "responseStatus": "FAILURE",
    "reason": "Invalid AI intake section object. Field \"height_value__v\" \
    with value \"999999\" in section \"patient\" is not valid. Error: \"The \
    input is outside of the supported range limits\". Please refer to documentation."
}
'''

Use the following endpoint to send JSON to Veeva Safety, which will be imported to a single Inbox Item:

POST `/api/{version}/app/safety/ai/intake`

Before submitting this request:

-   The User record for the API user must link to the Organization receiving the report in the **Organization** field. Edit User records in **Admin > Users & Groups**.
-   The API user must have the _Access API Vault Action_ permission in their permission set.

#### Headers

Name

Description

`Content-Type`

-   `multipart/form-data`: Use to pass a JSON file or JSON text in the `intake_json` parameter when passing another document in the `intake_form` parameter.
-   `application/json`: Use to pass JSON text as raw content.

#### Body

Name

Description

`intake_json`

The filepath for the JSON intake file, or the raw JSON text. Veeva Safety creates an Inbox Item using the JSON passed through this parameter. Note that Veeva Safety does not support bulk intake with this endpoint. A single API call is required for each Inbox Item. Ensure to use the correct [JSON format](/docs/#safety-json).

`intake_form`

The filepath for a source intake document. Veeva Safety attaches the file passed through `intake_form` to the Inbox Item and Inbound Transmission. The `Content-Type` must be `multipart/form-data` to use this parameter.

#### Query Parameters

Name

Description

`{API_Name}`

(Optional) To specify which organization to send the Inbox Item to, enter the Vault API Name for the Organization record. The default value is `vault_customer`. Note that the Organization record type must be Sponsor.

#### Response Details

On `SUCCESS`, the response includes the `jobID`, which you can use to retrieve the job status, and the `transmissionRecordId`, which you can use to find the Inbound Transmission record in your Vault.

On `FAILURE`, check the reason text in the response against your Vault configuration and JSON file format and content. To view detailed logs for a job, log into your Vault and go to **Admin > Operations > Job Status**, where you can view your job history and download logs.

You can track the job status using the [Retrieve Job Status](#RetrieveJobStatus) endpoint.

## Import Narrative

**Note**: To bulk import multiple narratives, use the [Bulk Import Narrative endpoint](#Bulk_Import_Narrative).

> Request

'''
curl -X POST \
https://myvault.veevavault.com/api/v25.2/app/safety/import-narrative \
-H 'Authorization: {SESSION_ID}' \
-H 'caseId: V2B000000000201' \
-H 'narrativeType: primary' \
-H 'narrativeLanguage: eng' \
-H 'Content-Type: text/plain' \
-d 'The patient took 500 mg cholecap at 2pm and started experiencing heart palpitations at 2:30pm...'
'''

> Response

'''
{
"responseStatus": "SUCCESS",
}
'''

Use the following endpoint to import narrative text into a Case narrative.

POST `/api/{version}/app/safety/import-narrative`

The request creates a narrative document for the destination Case, in the format of the E2B import narrative template. The narrative text sent in the body of this call is appended to the template content.

If a Case narrative document already exists for the given language, the request creates a new version of the document and appends the narrative text sent in the body of this call to the existing content.

Before submitting this request:

-   You must be assigned permissions to use the API and have the _Edit Document_ permission for the `draft__v` state of the `narrative_lifecycle__v` object.
-   The destination Case must exist.

#### Headers

Name

Description

`caseId`

Destination Case or Adverse Event Report ID.

`narrativeType`

For the main narrative, enter `primary`. For a narrative translation, enter `translation`.  
The primary narrative must exist before you can add a translation.

`narrativeLanguage`

Three-letter ISO 639-2 language code.  
Currently, the primary narrative must be English (`eng`).

`link_translation_to_primary`

Set to `true` to add the localized narrative document as a supporting document to the global (English) narrative document. This parameter only applies when the `narrativeType` is set to `translation` and the localized narrative document does not already exist. If omitted, defaults to `false`.

`Content-Type`

`text/plain`

#### Body

In the body of the request, enter the narrative text. You can import up to 100,000 characters of narrative text.

#### Response Details

On `SUCCESS`, the response only includes the `responseStatus`.

On `FAILURE`, the response also returns a message describing the reason for the failure.

## Bulk Import Narrative

> Request

'''
curl --location --request POST 'https://myvault.veevavault.com/api/v25.2/app/safety/import-narrative/batch'
--header 'Content-Type: multipart/form-data'
--header 'Accept: text/csv'
--header 'Authorization: {SESSION_ID}'
--form 'narratives=@"/directory/bulk-narrative-import.csv"'
'''

> Response

'''
{
    "responseStatus": "success__v",
    "responseDetails":
    {
        "import_id": "dc2daf9d-8549-4701-805a-c3f62a2aefa5",
        "result_uri": "/api/v25.2/app/safety/import-narrative/batch/dc2daf9d-8549-4701-805a-c3f62a2aefa5"
    }
}
'''

Use the following endpoint to bulk import case narratives into Veeva Safety:

POST `/api/{version}/app/safety/import-narrative/batch/`

This request imports text to create multiple narrative documents, in the format of the E2B import narrative template. This request can import primary narratives as well as narrative translations. Narrative translations can optionally be imported to a Localized Case in addition to the global Case.

If a Case narrative or translation already exists for the given language, the request creates a new version of the document populated with the text sent through the request.

This endpoint is asynchronous. The following limits apply to this endpoint:

-   The maximum batch size is 500
-   The maximum CSV input file size is 100 MB
-   Maximum characters per narrative is 200k
-   The CSV file cannot contain duplicate rows with the same `caseId` and `narrativeLanguage`

#### Headers

Name

Description

`content-type`

`multipart/form-data`

`accept`

`text/csv`

`X-VaultAPI-IntegrityCheck`

Optional: Set to `true` to perform additional integrity checks on the CSV file. If omitted, defaults to `false`.

`X-VaultAPI-MigrationMode`

Optional: Set to `true` to perform additional verifications on the `localizedCaseId`, including checking that the `caseId` refers to the related global Case and the `narrativeLanguage` matches the language on the Localized Case. If omitted, defaults to `false`.

`X-VaultAPI-ArchiveDocument`

Optional: If the Vault Document Archive feature is enabled, set to `true` to send the imported narrative documents directly to the document archive, or `false` to create the imported documents as active narratives. If omitted and the Vault Document Archive feature is enabled, the imported narrative documents are sent directly to the document archive.

#### Body Parameter

The request is sent through a CSV file.

Name

Description

`narratives`

The CSV file containing the narratives to be imported.

Click the button below to download a sample CSV file:

[![Download Sample CSV](../../images/download-csv-orange.svg)](/docs/sample-files/safety-sample-bulk-narrative.csv)

Consider the following requirements when preparing the CSV file:

-   The values in the input file must be UTF-8 encoded.
-   CSVs must follow the [standard format](https://datatracker.ietf.org/doc/html/rfc4180).
-   The file must use a comma (`,`) as the delimiter
-   If the narrative text contains commas, enclose each comma within double-quotation marks (`“,”`)
-   If the narrative text contains double-quotation marks, they must be escaped (`\”example\“`)

The CSV file must have the following columns:

Column

Description

`caseId`

The Case record ID.

`localizedCaseId`

Optional: If you are importing a localized narrative, specify the Localized Case record ID. The narrative document will be linked to both the global Case ( `caseId`) and Localized Case. The following requirements apply:

-   `narrativeType` must be `translation`
-   `narrativeLanguage` must match the language on the destination Localized Case.
-   `caseId` must match the global Case

**Note**: The `localizedCaseId` column is required, even when empty.

`narrativeType`

The following types are accepted:

-   `primary`: The primary Case narrative, used to populate the Narrative Text and Narrative Preview fields on the Case.
-   `translation`: A narrative Translation.

`narrativeLanguage`

The three-letter ISO language code for the narrative language. For example, `eng` is english.

`narrative`

Text of the narrative document.

#### Response Details

On `SUCCESS`, the response includes the following information:

Name

Description

`import_id`

The ID of the import request, which you can use along with the [Retrieve Bulk Import Status endpoint](#Retrieve_Bulk_Import_Status) to check the status of the operation.

`result_uri`

The URI path to retrieve the status of the operation with the [Retrieve Bulk Import Status endpoint](#Retrieve_Bulk_Import_Status).

On `FAILURE`, the response returns an error message describing the reason for the failure.

## Retrieve Bulk Import Status

> Request

'''
curl --location --request GET 'https://myvault.veevavault.com/api/v25.2/app/safety/import-narrative/batch/dc2daf9d-8549-4701-805a-c3f62a2aefa5' \
--header 'Authorization: {SESSION_ID}'
'''

> Response: Completed

'''
{
    "responseStatus": "completed__v",
    "responseDetails" : {
        "import_id": "dc2daf9d-8549-4701-805a-c3f62a2aefa5",
        "job_id": "203715",
        "start_time": "2021-11-30T19:17:38.669Z[GMT]",
        "end_time": "2021-11-30T19:17:47.996Z[GMT]",
        "total_narratives": 3,
        "completed_narratives": 3
    },
    "data": [
        {
            "status": "SUCCESS",
            "case_id": "V2B000000002001",
            "narrative_document_version": "12_0_2"
        },
        {
            "status": "SUCCESS",
            "case_id": "V2B000000002002",
            "narrative_document_version": "1_0_1"
        },
        {
            "status": "FAILED",
            "case_id": "V2B000000002003",
            "errors": [ { "type": "INVALID_DATA", "message": "Error message describing why this document version was not added." } ]
        }
    ]
}

'''

> Response: In Progress

'''
{
    "responseStatus": "in_progress__v",
    "responseDetails" : {
        "import_id" : "db1e69cc-171b-11ec-9621-0242ac130002",
        "start_time" : "2021-09-16 00:00:00.0",
        "total_narratives": 3,
        "completed_narratives": 1
    }
}
'''

Use the following endpoint to retrieve the status of a bulk narrative import:

GET `/api/{version}/app/safety/import-narrative/batch/{importId}`

#### URI Path Parameters

Name

Description

`importId`

The `import_id` of the bulk narrative import job, retrieved from the job request response details.

#### Response Details

If a bulk import job is complete, the response returns details of each narrative document.

If a bulk import job is incomplete, the response returns details of the job in progress.
