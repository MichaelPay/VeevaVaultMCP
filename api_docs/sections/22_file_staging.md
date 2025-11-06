<!-- 
VaultAPIDocs Section: # File Staging
Original Line Number: 37121
Generated: August 30, 2025
Part 22 of 38
-->

# File Staging

The following endpoints allow you to create and manage files and folders in your Vault’s file staging. Learn more about [file staging in Vault Help](https://platform.veevavault.help/en/lr/38653). To upload files larger than 50MB, see [Resumable Upload Sessions](#Resumable_Upload_Sessions). You must have the _Application: File Staging: Access_ permission to use the File Staging API.

## List Items at a Path

Return a list of files and folders for the specified path. Paths are different for Admin users (Vault Owners and System Admins) and non-Admin users. Learn more about [paths in the Vault API Documentation](/docs/#File_Staging_Path).

> Request

'''
curl -L -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/services/file_staging/items/Cholecap?recursive=true&limit=2
'''

> Response

'''
{
   "responseStatus": "SUCCESS",
   "responseDetails": {
       "next_page": "https://myvault.veevavault.com/api/v25.2/services/file_staging/items?cursor=g8qOy3WDCd84tyi%2Bx6KQCA%3D%3D%3AWjeuCSM6tbtmhJ00VpjHMlimit=2&recursive=true"
   },
   "data": [
       {
           "kind": "folder",
           "path": "/Cholecap-References",
           "name": "Cholecap-References"
       },
       {
           "kind": "file",
           "path": "/Cholecap-References/cholecap-akathisia",
           "name": "cholecap-akathisia",
           "size": 35642,
           "modified_date": "2020-10-07T16:28:38.000Z"
       }
   ]
'''

GET `/api/{version}/services/file_staging/items/{item}`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`item`

The absolute path to a file or folder. This path is specific to the authenticated user. Admin users can access the root directory. All other users can only access their own user directory.

#### Query Parameters

Name

Description

`recursive`

If `true`, the response will contain the contents of all subfolders. If not specified, the default value is `false`.

`limit`

Optional: The maximum number of items per page in the response. This can be any value between 1 and 1000. If omitted, the default value is 1000.

`format_result`

If set to `csv`, the response includes a `job_id`. Use the Job ID value to retrieve the [status](#retrieve-job-status) and results of the request.

#### Response Details

On `SUCCESS`, the response includes the following information:

Name

Description

`kind`

The kind of item. This can be either `file` or `folder`.

`path`

The absolute path, including file or folder `name`, to the item on file staging.

`name`

The name of the file or folder.

`size`

The size of the file in bytes. Not applicable to folders.

`modified_date`

The timestamp of when the file was last modified. Not applicable to folders.

`next_page`

The pagination URL to navigate to the next page of results if the number of results exceeds the number defined by a request’s `limit`. This URL contains a `cursor` query parameter, which is valid for 30 minutes from the time of the original query.

`item`

The path root for the query. Included in responses where `format_result = csv`.

## Download Item Content

Retrieve the content of a specified file from file staging. Use the `Range` header to create resumable downloads for large files, or to continue downloading a file if your session is interrupted.

> Request

'''
curl -L -X GET -H "Authorization: {SESSION_ID}" \
-H "Range: bytes=0-1000" \
https://myvault.veevavault.com/api/v25.2/services/file_staging/items/content/u10001400/Wonder Drug Survey.docx
'''

> Response Headers

'''
Content-Type: application/octet-stream;charset=UTF-8
Content-Disposition: attachment;filename="Wonder Drug Survey.docx"
Content-Range: bytes 0-1000/11737
'''

GET `/api/{version}/services/file_staging/items/content/{item}`

#### Headers

Name

Description

`Range`

Optional: Specifies a partial range of bytes to include in the download. Maximum 50 MB. Must be in the format `bytes={min}-{max}`. For example, `bytes=0-1000`.

#### URI Path Parameters

Name

Description

`item`

The absolute path to a file. This path is specific to the authenticated user. Admin users can access the root directory. All other users can only access their own user directory.

#### Response Details

On `SUCCESS`, Vault retrieves the content of the specified file. The HTTP Response Header `Content-Type` is set to `application/octet-stream` and the HTTP Response Header `Content-Disposition` contains a filename component which can be used when naming the local file. If a `range` header was specified in the request, the response also includes the `Content-Range` HTTP Response Header, which specifies the bytes downloaded, as well as the total for the file. In the example above, the `Content-Range` specifies a download of bytes 1-1000 of 11737 total bytes.

## Create Folder or File

Upload files or folders up to 50MB to file staging. To upload files larger than 50MB, see [Resumable Upload Sessions](#Resumable_Upload_Sessions). You can only create one file or folder per request.

> Request: Create a File

'''
curl -L -X POST -H "Authorization: {SESSION_ID}" \
-H "Accept: application/json" \
-H "Content-Type: multipart/form-data" \
-F "path=/Wonder Drug Reference.docx" \
-F "kind=file" \
-F "overwrite=true" \
-F "file=@/Wonder Drug Reference.docx"\
https://myvault.veevavault.com/api/v25.2/services/file_staging/items
'''

> Response

'''
{
   "responseStatus": "SUCCESS",
   "data": {
       "kind": "file",
       "path": "/Wonder Drug Reference.docx",
       "name": "Wonder Drug Reference.docx",
       "size": 11922,
       "file_content_md5": "3b2130fbfa377c733532f108b5e50411"
   }
}
'''

> Request: Create a Folder

'''
curl -L -X POST -H "Authorization: {SESSION_ID}" \
-H "Accept: application/json" \
-H "Content-Type: multipart/form-data" \
-F "path=/u10001400/cholecap2021" \
-F "kind=folder" \
https://myvault.veevavault.com/api/v25.2/services/file_staging/items
'''

> Response

'''
{
   "responseStatus": "SUCCESS",
   "data": {
       "kind": "folder",
       "path": "/u10001400/cholecap2021/",
       "name": "cholecap2021"
   }
}
'''

POST `/api/{version}/services/file_staging/items`

#### Headers

Name

Description

`Content-Type`

`multipart/form-data`

`Accept`

`application/json` (default) or `application/xml`

`Content-MD5`

Optional: The MD5 checksum of the file being uploaded.

#### Body Parameters

Name

Description

`kind`required

The kind of item to create. This can be either `file` or `folder`.

`path`required

The absolute path, including file or folder name, to place the item in file staging. This path is specific to the authenticated user. Admin users can access the root directory. All other users can only access their own user directory.

`overwrite`optional

If set to `true`, Vault will overwrite any existing files with the same name at the specified destination. For folders, this is always `false`.

#### File Upload

To upload a file, use the multi-part attachment with the file component `"file={file_name}"`. The maximum allowed file size is 50MB.

#### Uploading Files to the Inbox Directory

You can create _Staged_ documents by uploading files to the _Inbox_ directory on your Vault’s file staging. [Learn more in Vault Help](https://platform.veevavault.help/en/lr/38653#inbox-details).

## Update Folder or File

Move or rename a folder or file on file staging. You can move and rename an item in the same request.

> Request

'''
curl -L -X PUT -H "Authorization: {SESSION_ID}"\
-H "Content-Type: application/x-www-form-urlencoded" \
--data-urlencode "parent=/u10001400/cholecap-2021" \
--data-urlencode "name=cholecap-2021-brochure" \
https://myvault.veevavault.com/api/v25.2/services/file_staging/items/Cholecap-References/cholecap-brochure
'''

> Response

'''
{
   "responseStatus": "SUCCESS",
   "data": {
       "job_id": 100949,
       "url": "/api/v25.2/services/jobs/100949"
   }
}
'''

PUT `/api/{version}/services/file_staging/items/{item}`

#### Headers

Name

Description

`Content-Type`

`application/x-www-form-urlencoded`

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`item`

The absolute path to a file or folder. This path is specific to the authenticated user. Admin users can access the root directory. All other users can only access their own user directory.

#### Body Parameters

At least one of the following parameters is required:

Name

Description

`parent`conditional

When moving a file or folder, specifies the absolute path to the parent directory in which to place the file.

`name`conditional

When renaming a file or folder, specifies the new name.

#### Response Details

On `SUCCESS`, the response contains the following information:

Name

Description

`job_id`

The Job ID value to retrieve the status and results of the request.

`url`

URL to retrieve the current job status of this request.

#### Updating Files in the Inbox Directory

Renaming a file in your Vault’s _Inbox_ directory creates a new _Staged_ document in your Vault and does not rename, remove, or update the previously created corresponding _Staged_ document. [Learn more in Vault Help](https://platform.veevavault.help/en/lr/38653#inbox-details).

## Delete File or Folder

Delete an individual file or folder from file staging.

> Request

'''
curl -L -X DELETE -H "Authorization:{SESSION_ID}"" \
-H "Accept: application/json" \
https://myvault.veevavault.com/api/v25.2/services/file_staging/items/u10001400/promotional2021?recursive=true
'''

> Response

'''
{
   "responseStatus": "SUCCESS",
   "data": {
       "job_id": 100953,
       "url": "/api/v25.2/services/jobs/100953"
   }
}
'''

DELETE `/api/{version}/services/file_staging/items/{item}`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`item`

The absolute path to the file or folder to delete. This path is specific to the authenticated user. Admin users can access the root directory. All other users can only access their own user directory.

#### Query Parameters

Name

Description

`recursive`

Applicable to deleting folders only. If `true`, the request will delete the contents of a folder and all subfolders. The default is `false`.

#### Response Details

On `SUCCESS`, the response contains the following information:

Name

Description

`job_id`

The Job ID value to retrieve the status and results of the request.

`url`

URL to retrieve the current job status of this request.

#### Deleting Files in the Inbox Directory

Deleting files from your Vault’s _Inbox_ directory does not delete corresponding _Staged_ documents Vault created when the files were uploaded. [Learn more in Vault Help](https://platform.veevavault.help/en/lr/38653#inbox-details).

## Resumable Upload Sessions

Use resumable upload sessions to upload files larger than 50MB to file staging in three steps:

1.  **Create Resumable Upload Session**: Generate an `upload_session_id`, which you can use to upload file parts, resume an interrupted session, retrieve information about a session, and, if necessary, abort a session.
2.  **Upload File Parts**: Use the `upload_session_id` from step 1 to upload parts of a file to an upload session. File parts can be from 5-50MB by default, although limits for your Vault may vary.
3.  **Commit Upload Session**: After you upload all file parts, use this endpoint to end the session and make the completed, reassembled file available in file staging.

Use the additional helper endpoints in this section to manage upload sessions. Each Vault allows up to 50 active upload sessions at a time. By default, upload sessions remain active for 72 hours after creation. If a session expires before it is committed, Vault will auto-purge all parts of the upload.

### Create Resumable Upload Session

Initiate a multipart upload session and return an upload session ID.

> Request

'''
curl -L -X POST -H "Authorization: {SESSION_ID}" \
-H 'Accept: application/json' \
-H 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'path=Cholecap-Commercial-2021.mp4' \
--data-urlencode 'size=32862312' \
--data-urlencode 'overwrite=true'\
https://myvault.veevavault.com/api/v25.2/services/file_staging/upload
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "data": {
        "path": "/Cholecap-Commercial-2021.mp4",
        "name": "Cholecap-Commercial-2021.mp4",
        "id": "31a6aba21bf6e0005b718407a78739e6",
        "expiration_date": "2020-12-14T23:30:43.000Z",
        "created_date": "2020-12-11T23:30:43.000Z",
        "last_uploaded_date": "2020-12-11T23:30:43.000Z",
        "owner": 275657,
        "uploaded_parts": 0,
        "size": 32862312,
        "uploaded": 0,
        "overwrite": true
    }
}
'''

POST `/api/{version}/services/file_staging/upload`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### Body Parameters

Name

Description

`path`required

The absolute path, including file name, to place the file in the staging server. This path is specific to the authenticated user. Admin users can access the root directory. All other users can only access their own user directory.

`size`required

The size of the file in bytes. The maximum file size is 500GB.

`overwrite`optional

If set to `true`, Vault will overwrite any existing files with the same name at the specified destination.

#### Response Details

Upon SUCCESS, the response includes the following information:

Name

Description

`path`

The path to the file as specified in the request.

`id`

The upload session ID.

`expiration_date`

The timestamp of when the upload session will expire.

`created_date`

The timestamp of when the session was created.

`last_uploaded_date`

The timestamp of the last upload in this session. Because the session was just created, this will be the same as the `created_date`.

`owner`

The user ID of the Vault user who initiated the upload session.

`uploaded_parts`

The number of parts uploaded to the session so far. Because the session was just created, this will be 0.

`size`

The size of the file in bytes as specified in the request.

`uploaded`

The total size, in bytes, uploaded so far in the session. Because the session was just created, this will be 0.

### Upload to a Session

The session owner can upload parts of a file to an active upload session. By default, you can upload up to 2000 parts per upload session, and each part can be up to 50MB. Use the `Range` header to specify the range of bytes for each upload, or split files into parts and add each part as a separate file. Each part must be the same size, except for the last part in the upload session.

> Request

'''
curl -L -X PUT -H "Authorization: {SESSION_ID}" \
-H "Accept: application/json" \
-H "Content-Type: application/octet-stream" \
-H "Content-Length: 5242880" \
-H "X-VaultAPI-FilePartNumber: 2" \
--data-binary "@/chunk-ab." \
https://myvault.veevavault.com/api/v25.2/services/file_staging/upload/.lqX6rv1jbu5vABJoy5XoSZmQXTTJV_jwxO.kFuS.qISxQJDiFm0s_kfb8oRS9DBDGg--
'''

> Response

'''
{
   "responseStatus": "SUCCESS",
   "data": {
       "size": 5242880,
       "part_number": 2,
       "part_content_md5": "d6762077325b9ec3b75ada3b269e17d3"
   }
}
'''

PUT `/api/{version}/services/file_staging/upload/{upload_session_id}`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

`Content-Type`

`application/octet-stream`

`Content-Length`

The size of the file part in bytes. Parts must be at least 5MB in size, except for the last part uploaded in a session.

`Content-MD5`

Optional: The MD5 checksum of the file part being uploaded.

`X-VaultAPI-FilePartNumber`

The part number, which uniquely identifies a file part and defines its position within the file as a whole. If a part is uploaded using a part number that has already been used, Vault overwrites the previously uploaded file part. You must upload parts in numerical order. For example, you cannot upload part 3 without first uploading parts 1 and 2.

#### URI Path Parameters

Name

Description

`upload_session_id`

The upload session ID.

#### Response Details

Upon SUCCESS, the response includes the `size`, `part_number`, and `part_content_MD5` for the file part.

### Commit Upload Session

Mark an upload session as complete and assemble all previously uploaded parts to create a file.

> Request

'''
curl -L -X POST -H "Authorization: {SESSION_ID}" \
-H "Accept: application/json" \
-H "Content-Type: application/json" \
https://myvault.veevavault.com/api/v25.2/services/file_staging/upload/.lqX6rv1jbu5vABJoy5XoSZmQXTTJV_jwxO.kFuS.qISxQJDiFm0s_kfb8oRS9DBDGg--
'''

> Response

'''
{
   "responseStatus": "SUCCESS",
   "data": {
       "job_id": 100954
   }
}
'''

POST `/api/{version}/services/file_staging/upload/{upload_session_id}`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

`Content-Type`

`application/json`(default)

#### URI Path Parameters

Name

Description

`upload_session_id`

The upload session ID.

#### Response Details

On `SUCCESS`, Vault returns the `job_id` for the commit. Use the [Job Status](#retrieve-job-status) API to retrieve the job results. Upon successful completion of the job, the file will be available on the staging server.

### List Upload Sessions

Return a list of active upload sessions.

> Request

'''
curl -L -X GET -H "Authorization: {SESSION_ID}" \
-H "Accept: application/json" \
https://myvault.veevavault.com/api/v25.2/services/file_staging/upload
'''

> Response

'''
{
   "responseStatus": "SUCCESS",
   "data": [
       {
           "path": "/u10001400/Gludacta-2021/Gludacta-Flyer.docx",
           "id": "yYFg7jN_fZBmUD9Tj98RkL2yqtbTdIh17iy02nd5pby62oqVJLXv.R.ea1jSr786rgwpf7Vx3RmmQ--",
           "expiration_date": "2020-10-10T18:32:55.000Z",
           "created_date": "2020-10-07T18:32:55.000Z",
           "last_uploaded_date": "2020-10-07T19:27:07.000Z",
           "owner": 10001400,
           "uploaded_parts": 1,
           "size": 1273267,
           "uploaded": 1273267
       },
       {
           "path": "/u10001400/Gludacta-2021/GludactaPackageBrochure.pdf",
           "id": "JEtOyUb9i.DXVbtW7xZT7jWr2rNLWtdWrV7IPCo9aILqd.k8nlNNlG3SbplEVDJulPijrFwnelJw--",
           "expiration_date": "2020-10-10T19:11:57.000Z",
           "created_date": "2020-10-07T19:11:57.000Z",
           "last_uploaded_date": "2020-10-07T19:11:57.000Z",
           "owner": 10001400,
           "uploaded_parts": 0,
           "size": 1438827,
           "uploaded": 0
       },
       {
           "path": "/u10001400/cholecap-2021/Cholecap-Commercial-2021.mp4",
           "id": "TpE_3roGfhpCppmk9ltKaEAbb8.kWbZEe6xDuW3lNa42801RbIEPJaWG07xvwrITJgVmXDw3UVL1w--",
           "expiration_date": "2020-10-10T19:30:18.000Z",
           "created_date": "2020-10-07T19:30:18.000Z",
           "last_uploaded_date": "2020-10-07T19:38:29.000Z",
           "owner": 10001400,
           "uploaded_parts": 2,
           "size": 32862312,
           "uploaded": 10485760
       }
        ]
}
'''

GET `/api/{version}/services/file_staging/upload`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### Response Details

On `SUCCESS`, Vault lists all active upload sessions for a Vault, along with their fields and field values. Admin users will see upload sessions for the entire Vault, while non-Admin users will see their own sessions only.

Name

Description

`path`

The absolute path, including file name, to place the file in the staging server. This path is specific to the authenticated user. Admin users can access the root directory. All other users can only access their own user directory.

`id`

The upload session ID.

`expiration_date`

The timestamp of when the upload session will expire.

`created_date`

The timestamp of when the session was created.

`last_uploaded_date`

The timestamp of the last upload in this session. Because the session was just created, this will be the same as the `created_date`.

`owner`

The user ID of the Vault user who initiated the upload session.

`uploaded_parts`

The number of file parts uploaded so far.

`size`

The total size, in bytes, of the file when complete.

`uploaded`

The total number of bytes uploaded so far in the session.

### Get Upload Session Details

Retrieve the details of an active upload session. Admin users can get details for all sessions, while non-Admin users can only get details for sessions if they are the owner.

> Request

'''
curl -L -X GET -H "Authorization: {SESSION_ID}"\
-H "Accept: application/json" \
https://myvault.veevevault.com/api/v25.2/services/file_staging/upload/TpE_3roGfhpCppmk9ltKaEAbb8.kWbZEe6xDuW3lNa42801RbIEPJaWG07xvwrITJgVmXDw3UVL1w--
'''

> Response

'''
{
   "responseStatus": "SUCCESS",
   "data": {
       "path": "/u10001400/cholecap-2021/Cholecap-Commercial-2021.mp4",
       "id": "TpE_3roGfhpCppmk9ltKaEAbb8.kWbZEe6xDuW3lNa42801RbIEPJaWG07xvwrITJgVmXDw3UVL1w--",
       "expiration_date": "2020-10-10T19:30:18.000Z",
       "created_date": "2020-10-07T19:30:18.000Z",
       "last_uploaded_date": "2020-10-07T19:38:29.000Z",
       "owner": 10001400,
       "uploaded_parts": 2,
       "size": 32862312,
       "uploaded": 10485760
   }
}
'''

GET `/api/{version}/services/file_staging/upload/{upload_session_id}`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`upload_session_id`

The upload session ID.

#### Response Details

On `SUCCESS`, the response includes the following information:

Name

Description

`path`

The absolute path, including file name, to place the file in the staging server. This path is specific to the authenticated user. Admin users can access the root directory. All other users can only access their own user directory.

`id`

The upload session ID.

`expiration_date`

The timestamp of when the upload session will expire.

`created_date`

The timestamp of when the session was created.

`last_uploaded_date`

The timestamp of the last upload in this session.

`owner`

The user ID of the Vault user who initiated the upload session.

`uploaded_parts`

The total number of file parts uploaded so far.

`size`

The total size, in bytes, of the file when complete.

`uploaded`

The total number of bytes uploaded so far in the session.

### List File Parts Uploaded to Session

Return a list of parts uploaded in a session. You must be an Admin user or the session owner.

> Request

'''
curl -L -X GET -H "Authorization: {SESSION_ID}"\
-H "Accept: application/json" \
https://myvault.veevavault.com/api/v25.2/services/file_staging/upload/98f46c04fa7a65ff2e5eaf90fdf613ab/parts?limit=2
'''

> Response

'''
{
   "responseStatus": "SUCCESS",
   "responseDetails": {
       "next_page": "https://myvault.veevavault.com/api/v25.2/services/file_staging/upload/98f46c04fa7a65ff2e5eaf90fdf613ab/parts?cursor=%2BMTykDOd3PrccDRP%2F254mQ%3D%3D%3A%2BkGnLUB6M9iDNUZeJ6BgOdWKpFQ%2BC7Q0B8UHdPxfJ7U%3D&limit=2"
   },
   "data": [
       {
           "size": 5242880,
           "part_number": 1,
           "part_content_md5": "c24a2d4b1c4e03a9f4113903edac6f47"
       },
       {
           "size": 5242880,
           "part_number": 2,
           "part_content_md5": "d6762077325b9ec3b75ada3b269e17d3"
       }
   ]
}
'''

GET `/api/{version}/services/file_staging/upload/{upload_session_id}/parts`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`upload_session_id`

The upload session ID.

#### Query Parameters

Name

Description

`limit`

Optional: The maximum number of items per page in the response. This can be any value between 1 and 1000. If omitted, the default value is 1000.

#### Response Details

On `SUCCESS`, the response includes the `size` and `part_number` of each file part uploaded to the session so far. If the number of parts returned exceeds 1000 or the number defined by the `limit`, Vault includes pagination links in the response.

### Abort Upload Session

Abort an active upload session and purge all uploaded file parts. Admin users can see and abort all upload sessions, while non-Admin users can only see and abort sessions where they are the owner.

> Request

'''
curl -L -X DELETE -H "Authorization: {SESSION_ID}" \
-H "Accept: application/json" \
https://myvault.veevavault.com/api/v25.2/services/file_staging/upload/TpE_3roGfhpCppmk9ltKaEAbb8.kWbZEe6xDuW3lNa42801RbIEPJaWG07xvwrITJgVmXDw3UVL1w--
'''

> Response

'''
{
   "responseStatus": "SUCCESS"
}
'''

DELETE `/api/{version}/services/file_staging/upload/{upload_session_id}`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`upload_session_id`

The upload session ID.
