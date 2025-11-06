<!-- 
VaultAPIDocs Section: # Direct Data
Original Line Number: 783
Generated: August 30, 2025
Part 2 of 38
-->

# Direct Data

Direct Data API provides high-speed read-only data access to Vault. The following endpoints allow you to retrieve available Direct Data files and download them. Learn more about [Direct Data API](/directdata/).

To use Direct Data API endpoints, your Vault integration user’s security profile and permission set must grant the following permissions:

-   _Application: API: Access API_
-   _Application: API: Direct Data or Application: API: All API_
-   _Application: All Object Records: All Object Record Read_
-   _Application: Workflow: Query_
-   _Admin: Logs: System Audit_
-   _Admin: Logs: Login Audit_
-   _Admin: Logs: Object Record Audit_

Additionally, if your Vault uses documents, your Vault integration user’s security profile and permission set must also grant the following permissions:

-   _Application: All Documents: All Document Read_
-   _Admin: Logs: Document Audit_

## Retrieve Available Direct Data Files

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
-H "Accept: application/json" \
https://myvault.veevavault.com/api/v25.2/services/directdata/files
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "responseDetails": {
        "total": 2
    },
    "data": [
        {
            "name": "1000020-20250513-1330-N",
            "filename": "1000020-20250513-1330-N.tar.gz",
            "extract_type": "incremental_directdata",
            "start_time": "2025-05-13T13:15Z",
            "stop_time": "2025-05-13T13:30Z",
            "record_count": 0,
            "size": 47567,
            "fileparts": 1,
            "filepart_details": [
                {
                    "name": "1000020-20250513-1330-N.001",
                    "filename": "1000020-20250513-1330-N.tar.gz.001",
                    "filepart": 1,
                    "size": 47567,
                    "md5checksum": "fa7d8bcff8ae95f9f511d4e88dba852e",
                    "url": "https://promomats2.yanjunzhang-pvm-1.vaultpvm.com/api/v25.2/services/directdata/private/files/1000020-20250513-1330-N.001"
                }
            ]
        },
        {
            "name": "1000020-20250513-1345-N",
            "error": {
                "next_retry": "2025-05-13T14:15Z",
                "message": "Failed to publish incremental_directdata file. No other action is needed at this time."
            }
        }
    ]
}
'''

Retrieve a list of all Direct Data files available for download.

GET `/api/{version}/services/directdata/files`

#### Headers

Name

Description

`Accept`

`application/json` (default)

#### Query Parameters

Name

Description

`extract_type`

The Direct Data file type: `incremental_directdata`, `full_directdata`, or `log_directdata`. If omitted, returns all files. Learn more about [Direct Data file types](/directdata/#Understanding_Direct_Data_Files).

`start_time`

Specify a time in `YYYY-MM-DDTHH:MM:SSZ` format. For example, 7AM on January 15, 2024 would use `2024-01-15T07:00:00Z`. If omitted, defaults to the Vault’s creation date and time. All Full files have a start time of `2000-01-01T00:00:00Z`.

`stop_time`

Specify a time in `YYYY-MM-DDTHH:MM:SSZ` format. For example, 9AM on January 15, 2024 would use `2024-01-15T09:00:00Z`. If omitted, defaults to today’s date and current time.

#### Response Details

On `SUCCESS`, Vault lists all Direct Data files available for download.

The response includes the following metadata for each file that is published:

Metadata Field

Description

`name`

The name of the Direct Data file, excluding the .gzip extension.

`filename`

The name of the Direct Data .gzip file.

`extract_type`

The Direct Data file type: `incremental_directdata`, `full_directdata`, or `log_directdata`.

`start_time`

The start time in `YYYY-MM-DDTHH:MM:SSZ` format. If this query parameter is not provided in the request, the start time defaults to the Vault’s creation date and time.

`stop_time`

The stop time in `YYYY-MM-DDTHH:MM:SSZ` format. If the query parameter is not provided in the request, the stop time defaults to today’s date and current time.

`record_count`

The total number of records for all extracts in the file. This may show as zero records if there is no data for the given time period.

`size`

The size of the Direct Data file in bytes.

`fileparts`

The number of file parts for a given Direct Data file. Extract files greater than 1 GB in size are split into multiple file parts.

`filepart_details`

A list of all file parts and their metadata.

If Direct Data API fails to publish a file for a specific time interval, the response includes an `error` object containing the following metadata:

Metadata Field

Description

`next_retry`

The time at which to reattempt retrieval of the file, in UTC.

`message`

The error message describing the reason for failure.

If Direct Data API successfully publishes the file at the `next_retry` time, the response then includes the metadata for that file.

### Review Results
- **Location:** `veevavault/services/directdata/directdata_service.py`
- **Function:** `retrieve_available_direct_data_files`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.

## Download Direct Data File

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
-H "Accept: application/json" \
https://myvault.veevavault.com/api/v25.2/services/directdata/files/146478-20240211-0000-N.001
'''

> Response Headers

'''
Content-Type: application/octet-stream;charset=UTF-8
Content-Disposition: attachment; filename="146478-20240211-0000-N.tar.gz.001"
'''

Download a Direct Data file.

GET `/api/{version}/services/directdata/files/{name}`

#### Headers

Name

Description

`Accept`

`application/json` (default)

#### URI Path Parameters

Name

Description

`{name}`

The `name` of the Direct Data file part. Obtain this from the [Retrieve Available Direct Data Files](#Retrieve_Available_Direct_Data_Files) request. For example, `146478-20240213-0000-F.001`.

#### Response Details

On `SUCCESS`, Vault downloads the requested Direct Data file. The file is named according to the following format: `{vaultid}-{date}-{stoptime}-{type}.tar.gz.{filepart}`.

Until the first Full file is generated, no Incremental files are available for download. The API may return the following standard error if an Incremental file is unavailable for download:

`FAILURE: Initial file being generated. Please check again later.`

### Review Results
- **Location:** `veevavault/services/directdata/directdata_service.py`
- **Function:** `download_direct_data_file`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.
